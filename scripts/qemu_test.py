#!/usr/bin/env python3
"""Drive the unmodified xv6 make qemu target over stdin; no pip packages needed."""

import argparse
import os
from pathlib import Path
import re
import selectors
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
XV6 = ROOT / "xv6-riscv"


class QemuSession:
    def __init__(self, log_path, timeout):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.log = self.log_path.open("wb")
        self.timeout = timeout
        self.pending = b""
        self.process = None
        self.selector = selectors.DefaultSelector()

    def record(self, data):
        self.log.write(data)
        self.log.flush()
        sys.stdout.buffer.write(data)
        sys.stdout.buffer.flush()

    def start(self):
        self.record(b"[host] make -C xv6-riscv qemu\n")
        self.process = subprocess.Popen(
            ["make", "-C", str(XV6), "qemu"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            bufsize=0,
        )
        self.selector.register(self.process.stdout, selectors.EVENT_READ)
        self.expect(b"init: starting sh", 120)
        self.expect(b"$ ", 30)

    def expect(self, marker, timeout=None):
        deadline = time.monotonic() + (self.timeout if timeout is None else timeout)
        while True:
            if b"panic:" in self.pending:
                raise RuntimeError("xv6 kernel panic (see log)")
            if marker in self.pending:
                end = self.pending.index(marker) + len(marker)
                output, self.pending = self.pending[:end], self.pending[end:]
                return output
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError(f"waiting for {marker!r}")
            if not self.selector.select(remaining):
                raise TimeoutError(f"waiting for {marker!r}")
            data = os.read(self.process.stdout.fileno(), 65536)
            if not data:
                raise RuntimeError(
                    f"QEMU/make exited before {marker!r} (status {self.process.poll()})"
                )
            self.record(data)
            self.pending += data

    def command(self, command, expected):
        self.process.stdin.write(command.encode("ascii") + b"\n")
        self.process.stdin.flush()
        output = self.expect(b"$ ").replace(b"\r\n", b"\n")
        if b"FAILED" in output or b"NO TESTS EXECUTED" in output:
            raise RuntimeError(f"{command}: xv6 reported test failure")
        for pattern in expected:
            if not re.search(pattern, output, re.MULTILINE):
                raise RuntimeError(f"{command}: missing expected output {pattern!r}")
        return output

    def shutdown(self):
        if self.process is None or self.process.poll() is not None:
            return
        self.record(b"\n[host] QEMU exit: Ctrl-a x\n")
        self.process.stdin.write(b"\x01x")
        self.process.stdin.flush()
        self.process.wait(timeout=10)
        rest = self.process.stdout.read()
        if rest:
            self.record(rest)
        if self.process.returncode:
            raise RuntimeError(f"make qemu exit status: {self.process.returncode}")

    def close(self):
        # Kill the process group as well as make if a timeout or Ctrl-C occurs.
        if self.process is not None:
            try:
                os.killpg(self.process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                os.killpg(self.process.pid, signal.SIGKILL)
                self.process.wait()
            self.process.stdin.close()
            self.process.stdout.close()
        self.selector.close()
        self.log.close()


def main():
    parser = argparse.ArgumentParser(
        prog="scripts/test",
        description="xv6 を起動してテスト。既存の fs.img を使用し、ログを logs/ に保存。",
        epilog="例: scripts/test smoke / scripts/test -q / scripts/test name copyin",
    )
    parser.add_argument("mode", nargs="?", default="quick", choices=("smoke", "quick", "full", "name"))
    parser.add_argument("testname", nargs="?")
    parser.add_argument("-q", action="store_true", help="quick (usertests -q) の別名")
    args = parser.parse_args()
    if args.q and args.mode != "quick":
        parser.error("-q は他の mode と同時に指定できません")
    if args.mode == "name":
        if not args.testname or not re.fullmatch(r"[A-Za-z0-9_]+", args.testname):
            parser.error("name の後に usertests のテスト名を指定してください")
    elif args.testname:
        parser.error("テスト名は name mode のみ指定できます")
    default_timeout = {"smoke": 120, "quick": 600, "full": 1800, "name": 600}[args.mode]
    try:
        timeout = float(os.environ.get("XV6_TEST_TIMEOUT", default_timeout))
        if not 0 < timeout < float("inf"):
            raise ValueError
    except ValueError:
        parser.error("XV6_TEST_TIMEOUT は正の秒数で指定してください")
    label = args.mode + (f"-{args.testname}" if args.testname else "")
    log_path = os.environ.get("XV6_TEST_LOG", str(ROOT / "logs" / f"test-{label}.log"))
    session = QemuSession(log_path, timeout)
    started = time.monotonic()
    try:
        session.start()
        if args.mode == "smoke":
            session.command("ls", [rb"^README\s+2\s+\d+\s+\d+", rb"^usertests\s+2\s+"])
            session.command("echo XV6_SMOKE_OK", [rb"^XV6_SMOKE_OK$"])
            session.command("cat README", [rb"^xv6 is a re-implementation", rb"^BUILDING AND RUNNING XV6$"])
            session.command("forktest", [rb"^fork test OK$"])
        else:
            command = {"quick": "usertests -q", "full": "usertests", "name": f"usertests {args.testname}"}[args.mode]
            patterns = [rb"^ALL TESTS PASSED$"]
            if args.mode == "name":
                patterns.append(rb"^test " + args.testname.encode() + rb": ")
            session.command(command, patterns)
        session.shutdown()
        session.record(f"[host] PASS {label} ({time.monotonic() - started:.1f}s)\n".encode())
        return 0
    except (OSError, RuntimeError, TimeoutError, subprocess.TimeoutExpired, KeyboardInterrupt) as error:
        session.record(f"\n[host] FAIL {label}: {type(error).__name__}: {error}\n".encode())
        return 1
    finally:
        session.close()
        print(f"Log: {session.log_path}")


if __name__ == "__main__":
    raise SystemExit(main())

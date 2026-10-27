#!/usr/bin/env python3
"""Resolve <!-- xv6ref: path#symbol --> code references against xv6-riscv/."""

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
XV6_DIR = ROOT / "xv6-riscv"
DOCS_DIR = ROOT / "docs"
VERSIONS_FILE = ROOT / "VERSIONS.md"
LOCK_FILE = DOCS_DIR / "xv6refs.lock"
UPSTREAM_BLOB_BASE = "https://github.com/mit-pdos/xv6-riscv/blob"

FENCE_START_RE = re.compile(r"^\s*(`{3,}|~{3,})")
INLINE_OR_REF_RE = re.compile(r"(`+[^`]*`+|<!--\s*xv6ref:\s*([^>]+?)\s*-->)")


class RefError(Exception):
    """Raised when an xv6ref cannot be parsed, resolved, or verified."""


@dataclass(frozen=True)
class RefOccurrence:
    doc_rel: str
    ref: str
    path: str
    symbol: str
    line_no: int
    start_offset: int
    end_offset: int


@dataclass(frozen=True)
class ResolvedSnippet:
    ref: str
    path: str
    symbol: str
    start_line: int
    end_line: int
    snippet: str
    sha256: str
    lang: str

    def github_url(self, commit: str) -> str:
        return f"{UPSTREAM_BLOB_BASE}/{commit}/{self.path}#L{self.start_line}-L{self.end_line}"


def read_xv6_commit(versions_path: Path = VERSIONS_FILE) -> str:
    text = versions_path.read_text(encoding="utf-8")
    m = re.search(r"コミット ID:\s*`([0-9a-f]{40})`", text)
    if not m:
        raise RefError(f"{versions_path.name} から 40 桁の xv6 コミット ID を読み取れません")
    return m.group(1)


def parse_ref_spec(raw_spec: str, doc_rel: str, line_no: int) -> tuple[str, str, str]:
    spec = raw_spec.strip()
    if "#" not in spec or spec.count("#") != 1:
        raise RefError(
            f"{doc_rel}:{line_no}: 不正な参照形式 '{spec}'（'path#symbol' 形式で指定してください）"
        )
    rel_path, symbol = spec.split("#", 1)
    rel_path = rel_path.strip()
    symbol = symbol.strip()
    if not rel_path or not symbol or ".." in Path(rel_path).parts or rel_path.startswith("/"):
        raise RefError(f"{doc_rel}:{line_no}: 不正な参照パスまたはシンボル '{spec}'")
    return f"{rel_path}#{symbol}", rel_path, symbol


def find_refs_in_markdown(markdown_text: str, doc_rel: str) -> list[RefOccurrence]:
    occurrences: list[RefOccurrence] = []
    in_fence: tuple[str, int] | None = None
    offset = 0

    for line_idx, raw_line in enumerate(markdown_text.splitlines(keepends=True), start=1):
        line = raw_line.rstrip("\r\n")
        if in_fence is not None:
            fence_char, fence_len = in_fence
            if re.match(rf"^\s*{re.escape(fence_char)}{{{fence_len},}}\s*$", line):
                in_fence = None
            offset += len(raw_line)
            continue

        fence_match = FENCE_START_RE.match(line)
        if fence_match:
            marker = fence_match.group(1)
            in_fence = (marker[0], len(marker))
            offset += len(raw_line)
            continue

        for m in INLINE_OR_REF_RE.finditer(line):
            raw_spec = m.group(2)
            if raw_spec is None:
                continue
            ref, rel_path, symbol = parse_ref_spec(raw_spec, doc_rel, line_idx)
            occurrences.append(
                RefOccurrence(
                    doc_rel=doc_rel,
                    ref=ref,
                    path=rel_path,
                    symbol=symbol,
                    line_no=line_idx,
                    start_offset=offset + m.start(),
                    end_offset=offset + m.end(),
                )
            )
        offset += len(raw_line)

    return occurrences


def _strip_c_comments_and_literals(text: str) -> str:
    """Replace comments, string literals, and char literals with spaces while preserving newlines."""
    out = list(text)
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if ch == "/" and nxt == "/":
            while i < n and text[i] != "\n":
                out[i] = " "
                i += 1
        elif ch == "/" and nxt == "*":
            out[i] = " "
            out[i + 1] = " "
            i += 2
            while i < n:
                if text[i] == "*" and i + 1 < n and text[i + 1] == "/":
                    out[i] = " "
                    out[i + 1] = " "
                    i += 2
                    break
                if text[i] != "\n":
                    out[i] = " "
                i += 1
        elif ch in ('"', "'"):
            quote = ch
            out[i] = " "
            i += 1
            while i < n:
                if text[i] == "\\" and i + 1 < n:
                    if text[i] != "\n":
                        out[i] = " "
                    if text[i + 1] != "\n":
                        out[i + 1] = " "
                    i += 2
                    continue
                if text[i] == quote:
                    out[i] = " "
                    i += 1
                    break
                if text[i] != "\n":
                    out[i] = " "
                i += 1
        else:
            i += 1
    return "".join(out)


def _offset_to_line(line_starts: list[int], pos: int) -> int:
    """Convert 0-based char offset into 1-based line number."""
    lo, hi = 0, len(line_starts) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if line_starts[mid] <= pos:
            lo = mid + 1
        else:
            hi = mid - 1
    return hi + 1


def _extract_c_symbol(text: str, lines: list[str], symbol: str) -> tuple[int, int] | None:
    cleaned = _strip_c_comments_and_literals(text)
    line_starts: list[int] = []
    pos = 0
    for ln in text.splitlines(keepends=True):
        line_starts.append(pos)
        pos += len(ln)
    if not line_starts:
        return None

    # Precompute brace depth at every character offset in cleaned text.
    depth_at = [0] * (len(cleaned) + 1)
    depth = 0
    for idx, ch in enumerate(cleaned):
        depth_at[idx] = depth
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth = max(0, depth - 1)
    depth_at[len(cleaned)] = depth

    cleaned_lines = cleaned.splitlines()

    # 1. Try top-level C function definition: <symbol>(...) { ... }
    func_pat = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(symbol)}\s*\(")
    for m in func_pat.finditer(cleaned):
        if depth_at[m.start()] != 0:
            continue
        sig_line = _offset_to_line(line_starts, m.start())
        if lines[sig_line - 1].lstrip().startswith("#"):
            continue
        # Match parentheses of parameter list.
        p_idx = cleaned.find("(", m.start())
        p_depth = 0
        close_paren = -1
        for k in range(p_idx, len(cleaned)):
            if cleaned[k] == "(":
                p_depth += 1
            elif cleaned[k] == ")":
                p_depth -= 1
                if p_depth == 0:
                    close_paren = k
                    break
        if close_paren == -1:
            continue
        # Between ')' and '{', allow whitespace or __attribute__((...)) only (no ';').
        rest = cleaned[close_paren + 1 :]
        attr_or_ws = re.match(r"^(?:\s|__attribute__\s*\(\([^;{}]*\)\))*\{", rest)
        if not attr_or_ws:
            continue
        open_brace = close_paren + 1 + attr_or_ws.end() - 1
        close_brace = -1
        for k in range(open_brace + 1, len(cleaned)):
            if cleaned[k] == "}" and depth_at[k] == 1:
                close_brace = k
                break
        if close_brace == -1:
            continue

        start_line = sig_line
        while start_line > 1:
            prev_raw = lines[start_line - 2].strip()
            prev_clean = cleaned_lines[start_line - 2].strip()
            if not prev_clean:
                break
            if prev_raw.startswith("#"):
                break
            if prev_clean.endswith((";", "}", "{", ":")):
                break
            start_line -= 1

        end_line = _offset_to_line(line_starts, close_brace)
        return start_line, end_line

    # 2. Fallback: top-level struct/enum/union or array/object definition with { ... };
    decl_pat = re.compile(
        rf"(?:(?:struct|enum|union)\s+{re.escape(symbol)}\s*\{{|(?<![A-Za-z0-9_]){re.escape(symbol)}\s*(?:\[[^;{{}}]*\])?\s*(?:\([^;{{}}]*\))?\s*=\s*\{{)"
    )
    for m in decl_pat.finditer(cleaned):
        if depth_at[m.start()] != 0:
            continue
        open_brace = cleaned.rfind("{", m.start(), m.end())
        close_brace = -1
        for k in range(open_brace + 1, len(cleaned)):
            if cleaned[k] == "}" and depth_at[k] == 1:
                close_brace = k
                break
        if close_brace == -1:
            continue
        start_line = _offset_to_line(line_starts, m.start())
        while start_line > 1:
            prev_raw = lines[start_line - 2].strip()
            prev_clean = cleaned_lines[start_line - 2].strip()
            if not prev_clean or prev_raw.startswith("#") or prev_clean.endswith((";", "}", "{")):
                break
            start_line -= 1
        end_line = _offset_to_line(line_starts, close_brace)
        return start_line, end_line

    return None


def _strip_asm_comment(line: str) -> str:
    # Handle '#' line comments (excluding preprocessor '#include' at start if needed).
    stripped = line.lstrip()
    if stripped.startswith("#include") or stripped.startswith("#define"):
        return stripped
    idx = line.find("#")
    if idx != -1:
        line = line[:idx]
    return line.strip()


def _extract_asm_symbol(lines: list[str], symbol: str) -> tuple[int, int] | None:
    label_re = re.compile(rf"^{re.escape(symbol)}\s*:(?!:)")
    any_label_re = re.compile(r"^([A-Za-z_.$][A-Za-z0-9_.$]*)\s*:(?!:)")
    globl_re = re.compile(r"^\.(?:globl|global)\s+([A-Za-z_.$][A-Za-z0-9_.$]*)\b")
    section_re = re.compile(r"^\.section\b")

    label_idx = -1
    for i, raw in enumerate(lines):
        code = _strip_asm_comment(raw)
        if label_re.match(code):
            label_idx = i
            break
    if label_idx == -1:
        return None

    start_idx = label_idx
    if start_idx - 1 >= 0:
        prev1 = _strip_asm_comment(lines[start_idx - 1])
        m1 = globl_re.match(prev1)
        if m1 and m1.group(1) == symbol:
            start_idx -= 1
        elif prev1.startswith(".align") and start_idx - 2 >= 0:
            prev2 = _strip_asm_comment(lines[start_idx - 2])
            m2 = globl_re.match(prev2)
            if m2 and m2.group(1) == symbol:
                start_idx -= 2

    end_idx = len(lines) - 1
    saw_instruction = False
    for j in range(label_idx, len(lines)):
        code = _strip_asm_comment(lines[j])
        if j == label_idx:
            after_colon = code.split(":", 1)[1].strip()
            if after_colon:
                saw_instruction = True
            continue
        if not code:
            continue
        if section_re.match(code):
            end_idx = j - 1
            break
        mg = globl_re.match(code)
        if mg and mg.group(1) != symbol and saw_instruction:
            end_idx = j - 1
            break
        ml = any_label_re.match(code)
        if ml and ml.group(1) != symbol and saw_instruction:
            end_idx = j - 1
            break
        if not code.startswith("."):
            saw_instruction = True

    while end_idx > start_idx and not lines[end_idx].strip():
        end_idx -= 1

    return start_idx + 1, end_idx + 1


def _extract_perl_symbol(lines: list[str], symbol: str) -> tuple[int, int] | None:
    sub_re = re.compile(rf"^\s*sub\s+{re.escape(symbol)}\b")
    start_idx = -1
    for i, raw in enumerate(lines):
        if sub_re.match(raw):
            start_idx = i
            break
    if start_idx == -1:
        return None

    depth = 0
    opened = False
    for j in range(start_idx, len(lines)):
        raw = lines[j]
        in_single = False
        in_double = False
        k = 0
        while k < len(raw):
            ch = raw[k]
            if ch == "\\" and (in_single or in_double):
                k += 2
                continue
            if ch == "'" and not in_double:
                in_single = not in_single
            elif ch == '"' and not in_single:
                in_double = not in_double
            elif not in_single and not in_double:
                if ch == "#":
                    break
                if ch == "{":
                    depth += 1
                    opened = True
                elif ch == "}":
                    depth -= 1
                    if opened and depth == 0:
                        return start_idx + 1, j + 1
            k += 1
    return None


def resolve_ref(rel_path: str, symbol: str, xv6_dir: Path = XV6_DIR) -> ResolvedSnippet:
    ref = f"{rel_path}#{symbol}"
    target = (xv6_dir / rel_path).resolve()
    try:
        target.relative_to(xv6_dir.resolve())
    except ValueError as exc:
        raise RefError(f"{ref}: xv6-riscv ディレクトリ外のパスです") from exc

    if not target.is_file():
        raise RefError(f"{ref}: ファイル 'xv6-riscv/{rel_path}' が見つかりません")

    text = target.read_text(encoding="utf-8")
    lines = text.splitlines()
    suffix = target.suffix

    if suffix in (".c", ".h"):
        span = _extract_c_symbol(text, lines, symbol)
        lang = "c"
    elif suffix in (".S", ".s"):
        span = _extract_asm_symbol(lines, symbol)
        lang = "asm"
    elif suffix == ".pl":
        span = _extract_perl_symbol(lines, symbol)
        lang = "perl"
    else:
        raise RefError(f"{ref}: 未対応のファイル拡張子 '{suffix}' です")

    if span is None:
        raise RefError(
            f"{ref}: シンボル '{symbol}' が 'xv6-riscv/{rel_path}' 内に見つかりません"
        )

    start_line, end_line = span
    snippet = "\n".join(lines[start_line - 1 : end_line])
    digest = hashlib.sha256((snippet + "\n").encode("utf-8")).hexdigest()
    return ResolvedSnippet(
        ref=ref,
        path=rel_path,
        symbol=symbol,
        start_line=start_line,
        end_line=end_line,
        snippet=snippet,
        sha256=digest,
        lang=lang,
    )


def render_ref_markdown(resolved: ResolvedSnippet, commit: str) -> str:
    url = resolved.github_url(commit)
    short_commit = commit[:8]
    line_label = (
        f"L{resolved.start_line}"
        if resolved.start_line == resolved.end_line
        else f"L{resolved.start_line}–L{resolved.end_line}"
    )
    return (
        f"**ソース抜粋**: [`{resolved.path}` の `{resolved.symbol}`"
        f"（{line_label}, commit `{short_commit}`）]({url})\n\n"
        f'```{resolved.lang} linenums="{resolved.start_line}"\n'
        f"{resolved.snippet}\n"
        f"```"
    )


def expand_markdown_refs(
    markdown_text: str,
    doc_rel: str,
    commit: str | None = None,
    xv6_dir: Path = XV6_DIR,
) -> str:
    occurrences = find_refs_in_markdown(markdown_text, doc_rel)
    if not occurrences:
        return markdown_text
    if commit is None:
        commit = read_xv6_commit()

    parts: list[str] = []
    cursor = 0
    for occ in occurrences:
        try:
            resolved = resolve_ref(occ.path, occ.symbol, xv6_dir=xv6_dir)
        except RefError as exc:
            raise RefError(f"{doc_rel}:{occ.line_no}: {exc}") from exc
        parts.append(markdown_text[cursor : occ.start_offset])
        parts.append(render_ref_markdown(resolved, commit))
        cursor = occ.end_offset
    parts.append(markdown_text[cursor:])
    return "".join(parts)


def collect_all_doc_refs(docs_dir: Path = DOCS_DIR) -> list[RefOccurrence]:
    all_occ: list[RefOccurrence] = []
    for md_path in sorted(docs_dir.rglob("*.md")):
        doc_rel = md_path.relative_to(ROOT).as_posix()
        text = md_path.read_text(encoding="utf-8")
        all_occ.extend(find_refs_in_markdown(text, doc_rel))
    return all_occ


def build_lock_data(
    docs_dir: Path = DOCS_DIR,
    xv6_dir: Path = XV6_DIR,
    versions_path: Path = VERSIONS_FILE,
) -> tuple[dict, list[str]]:
    errors: list[str] = []
    try:
        commit = read_xv6_commit(versions_path)
    except RefError as exc:
        return {}, [str(exc)]

    try:
        occurrences = collect_all_doc_refs(docs_dir)
    except RefError as exc:
        return {}, [str(exc)]

    entries: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for occ in occurrences:
        key = (occ.doc_rel, occ.ref)
        if key in seen:
            continue
        seen.add(key)
        try:
            resolved = resolve_ref(occ.path, occ.symbol, xv6_dir=xv6_dir)
        except RefError as exc:
            errors.append(f"{occ.doc_rel}:{occ.line_no} ({occ.ref}): {exc}")
            continue
        entries.append(
            {
                "doc": occ.doc_rel,
                "ref": resolved.ref,
                "path": resolved.path,
                "symbol": resolved.symbol,
                "start_line": resolved.start_line,
                "end_line": resolved.end_line,
                "sha256": resolved.sha256,
            }
        )

    entries.sort(key=lambda e: (e["doc"], e["ref"]))
    return {"commit": commit, "references": entries}, errors


def write_lock_file(lock_data: dict, lock_path: Path = LOCK_FILE) -> None:
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path.write_text(
        json.dumps(lock_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def verify_against_lock(
    docs_dir: Path = DOCS_DIR,
    xv6_dir: Path = XV6_DIR,
    versions_path: Path = VERSIONS_FILE,
    lock_path: Path = LOCK_FILE,
) -> tuple[int, list[str]]:
    current_data, errors = build_lock_data(docs_dir, xv6_dir, versions_path)
    if errors:
        return 0, errors

    if not lock_path.is_file():
        return 0, [
            f"{lock_path.relative_to(ROOT).as_posix()} が存在しません（scripts/check-refs --update で生成してください）"
        ]

    try:
        locked_data = json.loads(lock_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return 0, [f"{lock_path.relative_to(ROOT).as_posix()} の JSON 解析に失敗しました: {exc}"]

    if locked_data.get("commit") != current_data["commit"]:
        errors.append(
            f"VERSIONS.md のコミット ID ({current_data['commit']}) が "
            f"{lock_path.relative_to(ROOT).as_posix()} ({locked_data.get('commit')}) と一致しません"
        )

    locked_map = {
        (item["doc"], item["ref"]): item for item in locked_data.get("references", [])
    }
    current_map = {
        (item["doc"], item["ref"]): item for item in current_data["references"]
    }

    for key, cur in sorted(current_map.items()):
        doc_rel, ref = key
        if key not in locked_map:
            errors.append(
                f"{doc_rel} ({ref}): {lock_path.relative_to(ROOT).as_posix()} に未登録の参照です"
                "（scripts/check-refs --update で更新してください）"
            )
            continue
        locked = locked_map[key]
        if cur["sha256"] != locked.get("sha256"):
            errors.append(
                f"{doc_rel} ({ref}): 抜粋内容のハッシュが {lock_path.relative_to(ROOT).as_posix()} と一致しません "
                f"(locked={locked.get('sha256', '')[:12]}..., current={cur['sha256'][:12]}...)"
            )
        elif (cur["start_line"], cur["end_line"]) != (
            locked.get("start_line"),
            locked.get("end_line"),
        ):
            errors.append(
                f"{doc_rel} ({ref}): 行範囲が {lock_path.relative_to(ROOT).as_posix()} と一致しません "
                f"(locked=L{locked.get('start_line')}-L{locked.get('end_line')}, "
                f"current=L{cur['start_line']}-L{cur['end_line']})"
            )

    for key in sorted(locked_map.keys() - current_map.keys()):
        doc_rel, ref = key
        errors.append(
            f"{doc_rel} ({ref}): {lock_path.relative_to(ROOT).as_posix()} に記録されていますが文書内から削除されています"
            "（scripts/check-refs --update で更新してください）"
        )

    return len(current_map), errors

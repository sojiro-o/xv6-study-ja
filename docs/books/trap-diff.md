# 第4章 和訳と現在のコードの差分メモ（トラップとシステムコール）

> - **対象とする本教材ページ**: [第4章 トラップとシステムコール（1）アプリからOSに処理を頼む](../ch04-syscall.md)
> - **全体の章・節対応**: [教科書との対応表](../books-map.md)
> - **照合した3つの版**:
>   1. **菅原訳（`books/sugawara-ja/trap.tex`）**: 第4章「トラップとデバイスドライバ」（2019-10-08 原文 `ca13de46` ベース、和訳コミット `de6c710a`）
>   2. **MIT 最新英語原文（`books/mit-en/trap.tex` ほか）**: Chapter 4 *Traps and system calls*（2026-09-23 コミット `fa3b46bc`）
>   3. **現在の `xv6-riscv/` コード**: `mit-pdos/xv6-riscv` コミット [`e93dabeb98431235c6e1a101cb96c73c923fdbc4`](https://github.com/mit-pdos/xv6-riscv/tree/e93dabeb98431235c6e1a101cb96c73c923fdbc4)（2026-10-26）

電気通信大学・菅原研究室による和訳は 2019 年版の英語原文をもとに翻訳されているため、約7年分の `xv6-riscv` の改良によって、現在のコードとは**関数名・構造体メンバ名・レジスタ退避手順・割り込み機構**などに多くの違いが生じています。

このページでは、和訳の第4章（`trap.tex`）とシステムコール周辺で実際にソースコードと照合して確認できた差分を一覧にまとめています。

---

## 1. 章の構成・節順の変化

コードの中身を見る前に、章そのものの構成が次のように再編されています。

| 項目 | 菅原訳（2019 年版ベース） | MIT 最新原文（2026 年版） |
| --- | --- | --- |
| **第4章のタイトル** | 第4章「トラップとデバイスドライバ」 | Chapter 4 *Traps and system calls* |
| **トラップ処理の区分（章冒頭）** | 「カーネル空間」「ユーザ空間」「タイマ割込」の**3ケース**と説明 | 「ユーザ空間からのトラップ」「カーネル空間からのトラップ」の**2ケース**に整理（タイマ割込も通常の S-mode トラップに統合されたため） |
| **節の説明順序** | **4.2 カーネル空間** → **4.3 ユーザ空間** の順 | **4.2 ユーザ空間（*Traps from user space*）** → 4.3〜4.4 システムコール → **4.5 カーネル空間（*Traps from kernel space*）** の順に入れ替え |
| **ページフォルトの扱い** | 「ユーザ空間に届く例外はすべて犯人のプロセスを殺す」と説明 | 遅延割り当て（`vmfault`）を処理するパスが追加され、**Chapter 5 *Page faults*** として独立章が新設 |
| **タイマ割込とドライバ（和訳 4.4, 4.7〜4.10節）** | 第4章の中に同居 | **Chapter 6 *Interrupts and device drivers*** として独立章へ分離 |

---

## 2. トラップの往復・レジスタ退避まわりの差分（和訳 4.1〜4.3節 ／ MIT 4.1〜4.2・4.5節）

| 項目 | 菅原訳の記述（2019 年版） | 現在の `xv6-riscv/` コード（2026-10） | MIT 最新原文での記述 |
| --- | --- | --- | --- |
| **ユーザ空間への復帰関数（`usertrapret` → `prepare_return`）と戻り方** | `usertrap()` の末尾で **`usertrapret()`** を呼び、`usertrapret()` からトランポリン内の `userret(satp, TRAPFRAME)` を関数ポインタで呼び出す（`a0` にページテーブル、`a1` に `TRAPFRAME`）。（4.3節） | **`usertrapret()` は存在しない**。`kernel/trap.c` の **`prepare_return()`** で `stvec`・`trapframe`・`sstatus`・`sepc` を設定したあと、`uint64 usertrap(void)` がユーザ用 `satp` 値を **`return satp;`** で返す。`uservec` が `jalr t0` で呼んでいるため、`a0` に `satp` が入った状態で直後の `userret` へ直接リターンする（`a1` 引数は廃止）。（※初回起動の `forkret()` のみ `trampoline_userret(satp)` を直接呼ぶ：`kernel/proc.c`） | 4.2節で `prepare_return` を呼んだあと、`usertrap` がユーザページテーブルを `a0` に入れて `trampoline` 内の `userret` へ `return` すると記述。 |
| **`sscratch` レジスタの使い方（`csrrw` 交換 → `csrw` 退避）** | カーネルが事前に `sscratch` に `TRAPFRAME` を入れておき、`uservec` 先頭の **`csrrw`** で `a0` と交換して `TRAPFRAME` 番地を得る。帰り道の `userret` でも再度 `sscratch` と交換して次回のトラップに備える。（4.1節・4.3節） | `sscratch` に `TRAPFRAME` を保持しておく仕組みは廃止。`kernel/trampoline.S` の `uservec` は **`csrw sscratch, a0`** で `a0` を退避した直後に **`li a0, TRAPFRAME`** で定数番地をロードし、`csrr t0, sscratch` で元の `a0` を `112(a0)` に保存する。`userret` では `sscratch` を使わず、`li a0, TRAPFRAME` から最後に `ld a0, 112(a0)` で復元する。 | 4.1節・4.2節とも現在のコードどおり（`csrw` で `a0` を `sscratch` に退避し、`li` で `TRAPFRAME` を `a0` に入れる説明）。 |
| **`struct proc` のトラップフレームメンバ名** | **`p->tf`**（例：`p->tf->a0`）。また「`p->tf` は物理アドレス」と説明。（4.3節・4.5節・4.6節） | `kernel/proc.h` で **`struct trapframe *trapframe;`**（**`p->trapframe`**、例：`p->trapframe->a0`, `p->trapframe->epc`）。※カーネルは物理メモリを同一値で直接マップしているため、カーネル仮想アドレスとして扱う。 | 4.2節・4.3節で `p->trapframe`（“contains a kernel virtual address”）、`p->trapframe->a0` と記述。 |
| **ユーザ空間の例外・ページフォルト処理** | `syscall` でも `devintr` でもなければすべて不正例外とみなし、プロセスを殺す。（4章冒頭・4.3節） | `kernel/trap.c` の `usertrap()` に `r_scause() == 15 \|\| r_scause() == 13` の分岐があり、**`vmfault(p->pagetable, p->sz, r_stval(), ...)`** で遅延割り当てページを解決できれば実行を継続する。解決できない例外のみ `printk` して `setkilled(p)` → `kexit(-1)` する。 | 4章冒頭・4.2節でページフォルト時に `vmfault` を呼ぶと明記（詳細は第5章 *Page faults*）。 |
| **プロセスの kill フラグ判定・設定** | 構造体フィールド `p->killed` を直接読み書きする前提。 | ロック保護付きの関数 **`killed(p)`** と **`setkilled(p)`**（`kernel/proc.c`）を使う実装に変更（`kernel/trap.c` L57, L78, L81）。 | 第9章（9.4〜9.5節）のロック規則に合わせて整理。 |
| **`kernelvec.S` で保存するレジスタ** | `kernelvec` は「**全てのレジスタ**を退避します」と記述。（4.2節） | `kernel/kernelvec.S` は C の呼び出し先保存レジスタ（`s0`〜`s11`）を省き、**caller-saved レジスタのみ**をスタックに保存・復元する（また CPU コア移動に備えて `tp` も上書き復元しない）。 | 4.5節で “pushes all caller-saved registers onto the current stack” と記述。 |

---

## 3. システムコール呼び出し・引数・内部関数名の差分（和訳 4.5〜4.6節ほか ／ MIT 4.3〜4.4節ほか）

| 項目 | 菅原訳の記述（2019 年版） | 現在の `xv6-riscv/` コード（2026-10） | MIT 最新原文での記述 |
| --- | --- | --- | --- |
| **最初のシステムコールの例と `user/initcode.S` の廃止** | 最初のユーザプロセスが **`user/initcode.S`** のアセンブリから `SYS_exec` を `a7` に入れて `exec("/init", ...)` を呼ぶ流れを題材に `syscall()` を説明。（2.6節・4.5節） | **`user/initcode.S` は削除され存在しない**。最初のプロセスは `kernel/proc.c` の `forkret()`（`first == 1`）からカーネル内で直接 **`kexec("/init", ...)`** を呼んで起動する。通常のアプリは `user/usys.pl` が生成する `user/usys.S` のスタブ経由でシステムコールを呼ぶ。 | 2.6節は `forkret` が `kexec` を呼ぶ説明に変更。4.3節の例題も、シェルの `write(2, "$ ", 2)` → `user/usys.S` の `write:` スタブ → `SYS_write`（16）→ `sys_write` に全面変更。 |
| **カーネル内のコンソール出力関数（`printf` → `printk`）** | カーネル内でもユーザ空間と同名の **`printf`**（`kernel/printf.c`）を使用。（4.5節の未知システムコール番号エラー表示など） | ユーザ空間の `printf`（`user/printf.c`）と区別するため、ファイル名ごと **`kernel/printk.c` の `printk()`** に改名（例：`syscall()` 内の `printk("%d %s: unknown sys call %d\n", ...)`）。 | 第2章（`first.tex`）等で `kernel/printk.c` を参照。 |
| **システムコール本体のカーネル内部関数名（`k*` への改名）** | ユーザ関数名と同じ `exec`、`kill`、`fork`、`exit`、`wait` がカーネル内にもあった。 | 名前衝突・混同を避けるため、カーネル内部の実装関数に **`k` プレフィックス**が付いた：<br>・`sys_exec` → **`kexec`**（`kernel/exec.c`）<br>・`sys_kill` → **`kkill`**（`kernel/proc.c`）<br>・`sys_fork` → **`kfork`**（`kernel/proc.c`）<br>・`sys_exit` → **`kexit`**（`kernel/proc.c`）<br>・`sys_wait` → **`kwait`**（`kernel/proc.c`） | 2.6節・3.7節で `kexec`、9.4節で `kwait`・`kexit`・`kkill` として記述。 |
| **`sbrk` のスタブ名と2引数化（遅延割り当て対応）** | `usys.pl` は `sbrk:` ラベルを生成し、`sys_sbrk` は増減バイト数 `n` の1引数のみで即座に `growproc(n)` を呼んでいた。（和訳 3.7節） | `user/usys.pl` は **`sbrk` のみ `sys_sbrk` ラベル**を生成し、`user/ulib.c` の `sbrk(n)`（`SBRK_EAGER`）と `sbrklazy(n)`（`SBRK_LAZY`）が第2引数を渡して `sys_sbrk` を呼ぶ。`kernel/sysproc.c` の `sys_sbrk` は2引数 `(n, t)` を受け取り、遅延割り当て時は `myproc()->sz += n` のみ行う。 | 新設の第5章（`pgfault.tex` 5.1〜5.2節）で `SBRK_LAZY` / `SBRK_EAGER` と `sys_sbrk` を解説。 |
| **一時停止システムコールの改名（`sleep` → `pause`）と `sync` の追加** | 一時停止システムコールは **`SYS_sleep` / `sys_sleep`**（ユーザ側 `sleep(int)`）。システムコールは全21個。 | カーネル内部の `sleep()` 関数との混同を避けるため、システムコールは **`SYS_pause` / `sys_pause`**（ユーザ側 `pause(int)`）に改名。さらに22番として **`SYS_sync` / `sys_sync`** が追加された（`kernel/syscall.h`, `kernel/syscall.c`）。 | 第1章や第6章 6.4節などで `pause` システムコールとして記述。 |
| **`argint` / `argaddr` の戻り値型** | 「`argint`, `argaddr`, `argfd` 関数は *n* 番目のシステムコール引数を返します」と記述。（4.6節） | `kernel/syscall.c` の **`argint(int n, int *ip)` と `argaddr(int n, uint64 *ip)` の戻り値型は `void`**（常に成功しポインタ経由で格納。妥当性検査は後の `copyin` 等で行う）。なお `argstr` と `argfd` は `int`（負値でエラー）を返す。 | 4.4節で “retrieve the *n*'th system call argument from the trap frame” と表現を修正。 |
| **`copyout` / `copyin` / `copyinstr` の引数追加と `vmfault` 連携** | `copyinstr(pagetable, dst, srcva, max)` の4引数で、`walkaddr` が `0` なら即エラー。（4.6節） | `kernel/vm.c` の3関数すべてで第2引数にプロセスサイズ **`uint64 psz`** が追加された（例：`copyinstr(p->pagetable, p->sz, buf, addr, max)`）。未マップ（`pa0 == 0`）のときは **`vmfault(...)`** を呼んで遅延割り当てページの解決を試みる。 | 4.4節で基本構造を説明し、第5章冒頭で `kernel/vm.c` 内の `vmfault` 呼び出し箇所を読むよう案内。 |

---

## 4. 和訳第4章に含まれるタイマ割込・コンソールドライバの差分（和訳 4.4・4.7〜4.10節 → MIT 第6章）

和訳の第4章を通読すると、後半のタイマ割込やコンソールドライバでも現在のコードと大きく異なる箇所が出てきます。

| 項目 | 菅原訳の記述（4.4・4.8・4.10節） | 現在の `xv6-riscv/` コード（2026-10） | MIT 最新原文での記述（第6章 `interrupt.tex`） |
| --- | --- | --- | --- |
| **タイマ割込の仕組み（M-mode `CLINT` + `timervec` → S-mode `stimecmp` + `clockintr`）** | タイマ割込はマシンモードでしか受けられないため、`start.c` の `timerinit()` が `CLINT` とスクラッチ領域、`mtvec = timervec` を設定し、`kernelvec.S` の **`timervec`** がソフトウェア割込を起こして S-mode の `devintr` に渡すと説明。（4.1節・4.4節） | **`CLINT` スクラッチ領域も `kernelvec.S` の `timervec` も完全に削除**。RISC-V の **`sstc` 拡張**（`MENVCFG_STCE` と `stimecmp` CSR）を使い、`start.c` でタイマ割込も S-mode に直接委譲する。割込時は直接 `usertrap` / `kerneltrap` → `devintr()`（`scause == 0x8000000000000005L`）に入り、**`clockintr()`**（`kernel/trap.c`）が `ticks` 更新と次回の `w_stimecmp(r_time() + 1000000)` を行う。 | 第6章 6.4節 *Timer interrupts* に移動し、`time` / `stimecmp` レジスタと `clockintr` の説明に全面刷新。 |
| **コンソール出力と `uartputc`（ポーリング → 割込駆動 `uartwrite` ＋ `uartputc_sync`）** | 練習問題1（4.10節）で「`uartputc` は出力完了までポーリングして待つので、割込を使うように書き換えよ」と出題。 | `kernel/uart.c` では、ユーザの `write` システムコールからの出力（`consolewrite` → **`uartwrite`**）が**すでに送信完了割込と `sleep` を使う実装**になっている。ポーリングで1文字出す関数は `printk` とエコー専用の **`uartputc_sync`** に改名された。 | 第6章 6.2節 *Code: Console output* が新設されて `consolewrite` / `uartwrite` を解説。6.6節の練習問題1は逆に「割込を一切使わないように `uart.c` を書き換えよ」に変更。 |
| **カーネル内の `sleep` 呼び出し方法** | `consoleread` 内で `sleep(&cons.r, &cons.lock)` の1関数呼び出しとして参照。（4.8節） | `kernel/proc.c` の仕様変更により、**`sleep_prepare(&cons.r)` → `release(&cons.lock)` → `sleep()`**（引数なし）の順で呼ぶ2段階方式に変更されている（`kernel/console.c` L104-106、`kernel/uart.c` L89-91、`kernel/sysproc.c` L83-85）。 | 第6章 6.1節の行参照が新しい `sleep()` 呼び出しに更新され、詳細は第9章 *Sleep and Wakeup* で解説。 |

---

## 5. 菅原訳 `trap.tex` 内のコード参照（`\lineref`）照合一覧

菅原訳の本文中に登場する `\lineref{ファイル:検索パターン}` のうち、現在の `xv6-riscv/` で**そのままでは見つからないもの（ファイル廃止・関数改名・実装変更）**と、現在の対応箇所の一覧です。

| 菅原訳の節 | 菅原訳 `trap.tex` の参照指定 | 現在の状態 | 現在の `xv6-riscv/` で見るべき場所 |
| --- | --- | --- | --- |
| 4.3 ユーザ空間からのトラップ | `kernel/trap.c:/^usertrapret/` | **関数廃止** | `kernel/trap.c` の **`prepare_return`**（L101〜）および **`usertrap`** 末尾の `return satp;`（L88〜95） |
| 4.4 タイマ割込 | `kernel/trap.c:/machine-mode.timer/` | **記述削除** | `kernel/trap.c` の **`devintr`** 内 `scause == 0x8000000000000005L` 分岐（L213〜216）と **`clockintr`**（L167〜180） |
| 4.4 タイマ割込 | `kernel/kernelvec.S:/^timervec/` | **ラベル削除** | 廃止（`kernel/start.c` の **`timerinit`** L56〜66 で `stimecmp` を設定し S-mode で直接受信） |
| 4.5 Code: システムコールを呼ぶ | `user/initcode.S:/SYS_exec/` | **ファイル廃止** | 初回 `/init` 起動は `kernel/proc.c` の **`forkret`**（L522〜536 の `kexec`）。ユーザ側の `ecall` スタブは **`user/usys.pl`**（ビルド後は `user/usys.S`） |
| 4.8 Code: コンソールドライバ | `kernel/console.c:/sleep..cons/` | **呼び出し形式変更** | `kernel/console.c` の **`consoleread`** 内 `sleep_prepare(&cons.r)` → `release(&cons.lock)` → `sleep()`（L104〜106） |
| 4.10 練習問題 | `kernel/uart.c:/^uartputc/` | **関数改名・役割分離** | ポーリング出力は `kernel/uart.c` の **`uartputc_sync`**（L107〜124）、割込駆動出力は **`uartwrite`**（L81〜100） |

> 上記以外の `trap.tex` 内の参照（`kernel/trampoline.S` の `uservec` / `userret`、`kernel/trap.c` の `usertrap` / `kerneltrap` / `devintr`、`kernel/kernelvec.S` の `kernelvec`、`kernel/proc.h` の `struct trapframe`、`kernel/syscall.c` の `syscall` / `syscalls` / `argraw` / `fetchstr`、`kernel/vm.c` の `copyinstr` / `walkaddr` など）は、現在の `xv6-riscv/` でも同じファイル・関数名で存在します（ただし内部の細部は上記2〜4節のとおり更新されています）。

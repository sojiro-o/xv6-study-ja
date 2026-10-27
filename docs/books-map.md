# 教科書との対応表（MIT 最新版・菅原訳・本教材）

このリポジトリでは、学習者が普段読んでいる **MIT の xv6 教科書（英語原文）** と **電気通信大学・菅原研究室による日本語訳** の2冊と対応づけながら学べるように、本教材（`docs/`）の章番号を **MIT 教科書の最新版（全13章）** に合わせています。

それぞれのソースは参照用として `books/` ディレクトリに無改変で収録しています（出典とコミットの詳細はリポジトリ直下の `books/README.md` および `VERSIONS.md` を参照）。

| 資料 | 配置先 / 対象 | 版・コミット | 章数 |
| --- | --- | --- | --- |
| **MIT 教科書（最新英語原文）** | `books/mit-en/` | [`mit-pdos/xv6-riscv-book`](https://github.com/mit-pdos/xv6-riscv-book) `fa3b46bc`（2026-09-23） | 全13章（＋序文） |
| **菅原研究室による和訳** | `books/sugawara-ja/` | [`sugawara-bbbb/xv6-riscv-book`](https://github.com/sugawara-bbbb/xv6-riscv-book) `de6c710a`（2020-07-23）<br>※元になった英語原文は `ca13de46`（2019-10-08） | 全9章（＋序文） |
| **本リポジトリのコードと教材** | `xv6-riscv/` / `docs/` | [`mit-pdos/xv6-riscv`](https://github.com/mit-pdos/xv6-riscv/tree/e93dabeb98431235c6e1a101cb96c73c923fdbc4) `e93dabeb`（2026-10-26） | 章番号は MIT 最新版に準拠 |

---

## 1. 章立ての変化の要点（2019 年版ベースの和訳 → MIT 最新版）

菅原訳の元になった 2019 年版（全9章）から MIT 最新版（全13章）にかけて、**1章の新設**と**3か所の章分割**が行われたため、**第5章以降は章番号がずれています**。

| MIT 最新版（`books/mit-en/`） | 菅原訳（`books/sugawara-ja/`） | 主な構成変更（増減・分割・移動） |
| --- | --- | --- |
| Foreword and acknowledgments（`acks.tex`） | 序文と謝辞（`acks.tex`） | 章番号なし（共通） |
| **Ch.1** Operating system interfaces（`unix.tex`） | **第1章** オペレーティングシステムのインタフェース（`unix.tex`） | 章・節構成は同一（1.1〜1.6） |
| **Ch.2** Operating system organization（`first.tex`） | **第2章** オペレーティングシステムの構成（`first.tex`） | **2.7 *Security Model* が新設**（以降の節番号が +1）。2.6節も `initcode.S` 廃止に伴い内容更新 |
| **Ch.3** Page tables（`mem.tex`） | **第3章** ページテーブル（`mem.tex`） | 和訳の **3.7 `Code: sbrk` が第3章から外れ、新設の Ch.5 へ発展・移動**（3.8〜3.10 → 3.7〜3.9 へ繰り上がり） |
| **Ch.4** Traps and system calls（`trap.tex`） | **第4章** トラップとデバイスドライバ（`trap.tex`）の前半 | 章題が変更。タイマ割込とドライバが **Ch.6** へ分離。また「カーネル空間／ユーザ空間」の**節の順序が入れ替わり**、ユーザ空間（4.2）が先に移動 |
| **Ch.5** Page faults（`pgfault.tex`） | **対応する章なし**（旧 3.7 `Code: sbrk` が関連） | **新設章**。`sbrk` の遅延割り当て（lazy allocation）や COW fork、デマンドページング、mmap を扱う |
| **Ch.6** Interrupts and device drivers（`interrupt.tex`） | **第4章** トラップとデバイスドライバの後半（4.4・4.7〜4.10節） | **第4章から分離独立**。コンソール出力（6.2）とドライバの並行性（6.3）が独立節として追加され、タイマ割込（6.4）は後方に移動し `stimecmp` 方式へ刷新 |
| **Ch.7** Locking（`lock.tex`） | **第5章** ロック（`lock.tex`） | 章番号が **5 → 7** に移動。**7.7 *Programming with Atomics* が新設** |
| **Ch.8** Scheduling（`sched.tex`） | **第6章** スケジューリング（`sched.tex`）の前半（6.1〜6.4節） | 和訳の第6章が **Ch.8 と Ch.9 に2分割**。8.2 *Context switch overview* が独立節化 |
| **Ch.9** Sleep and Wakeup（`sleep.tex`） | **第6章** スケジューリングの後半（6.5〜6.8節） | **第6章後半が独立章に分離**。**9.5 *Process Locking* が新設** |
| **Ch.10** File system（`fs.tex`） | **第7章** ファイルシステム（`fs.tex`）のロギング以外 | 章番号が **7 → 10** に移動。途中にあったロギング層（和訳 7.4〜7.6節）が **Ch.11** として後ろへ分離 |
| **Ch.11** Logging（`log.tex`） | **第7章** ファイルシステムのロギング部分（7.4〜7.6節） | **第7章から分離独立** |
| **Ch.12** Concurrency revisited（`lock2.tex`） | **第8章** 並行性・再び（`lock2.tex`） | 章番号が **8 → 12** に移動。節構成（1〜5）は同一 |
| **Ch.13** Summary（`sum.tex`） | **第9章** まとめ（`sum.tex`） | 章番号が **9 → 13** に移動（節なし） |

---

## 2. 全章・全節の対応一覧

見出しは各教科書の LaTeX ソース（`\chapter` / `\section`）からそのまま採取しています。

### 序文（`acks.tex`）

| MIT 最新版（`books/mit-en/`） | 菅原訳（`books/sugawara-ja/`） | 本リポジトリの教材 | 備考 |
| --- | --- | --- | --- |
| Foreword and acknowledgments | 序文と謝辞 | — | `\chapter*`（章番号なし） |

### 第1章：OS のインタフェース（`unix.tex`）

| MIT 最新版（Ch.1 *Operating system interfaces*） | 菅原訳（第1章「オペレーティングシステムのインタフェース」） | 本リポジトリの教材 | 備考 |
| --- | --- | --- | --- |
| 1.1 Processes and memory | 1.1 プロセスとメモリ | 未作成 | |
| 1.2 I/O and File descriptors | 1.2 I/O とファイルディスクリプタ | 未作成 | |
| 1.3 Pipes | 1.3 パイプ | 未作成 | |
| 1.4 File system | 1.4 ファイルシステム | 未作成 | |
| 1.5 Real world | 1.5 世の中のオペレーティングシステム | 未作成 | |
| 1.6 Exercises | 1.6 練習問題 | 未作成 | |

### 第2章：OS の構成（`first.tex`）

| MIT 最新版（Ch.2 *Operating system organization*） | 菅原訳（第2章「オペレーティングシステムの構成」） | 本リポジトリの教材 | 備考 |
| --- | --- | --- | --- |
| 2.1 Abstracting physical resources | 2.1 物理的なリソースの抽象化 | 未作成 | |
| 2.2 User mode, supervisor mode, and system calls | 2.2 ユーザモード，スーパーバイザモード，およびシステムコール | 未作成（一部 [第4章（1）](ch04-syscall.md) 3節で導入） | |
| 2.3 Kernel organization | 2.3 カーネルの構成 | 未作成 | |
| 2.4 Code: xv6 organization | 2.4 Code: xv6 の構成 | 未作成 | |
| 2.5 Process overview | 2.5 プロセスの概要 | 未作成 | |
| 2.6 Code: Starting xv6, the first process and system call | 2.6 Code: xv6 の起動と最初のプロセス | 未作成 | 最新版は `initcode.S` 廃止に伴い `forkret` → `kexec("/init", ...)` 方式へ変更 |
| 2.7 Security Model | —（対応する節なし） | 未作成 | **最新版で新設** |
| 2.8 Real world | 2.7 世の中のオペレーティングシステム | 未作成 | 節番号 2.7 → 2.8 |
| 2.9 Exercises | 2.8 練習問題 | 未作成 | 節番号 2.8 → 2.9 |

### 第3章：ページテーブル（`mem.tex`）

| MIT 最新版（Ch.3 *Page tables*） | 菅原訳（第3章「ページテーブル」） | 本リポジトリの教材 | 備考 |
| --- | --- | --- | --- |
| 3.1 Paging hardware | 3.1 ページングハードウェア | 未作成 | |
| 3.2 Kernel address space | 3.2 カーネルのアドレス空間 | 未作成 | |
| 3.3 Code: Creating an address space | 3.3 Code: アドレス空間を作る | 未作成 | |
| 3.4 Physical memory allocation | 3.4 物理メモリのアロケート | 未作成 | |
| 3.5 Code: Physical memory allocator | 3.5 Code: 物理メモリのアロケータ | 未作成 | |
| 3.6 Process address space | 3.6 プロセスのアドレス空間 | 未作成 | |
| —（Ch.5 の 5.1〜5.2 へ発展・移動） | 3.7 Code: sbrk | 未作成 | **和訳 3.7節は第3章から削除され、Ch.5（*Page faults*）へ統合** |
| 3.7 Code: exec | 3.8 Code: exec | 未作成 | 節番号 3.8 → 3.7（関数名は `kexec` に変更） |
| 3.8 Real world | 3.9 世の中のオペレーティングシステム | 未作成 | 節番号 3.9 → 3.8 |
| 3.9 Exercises | 3.10 練習問題 | 未作成 | 節番号 3.10 → 3.9 |

### 第4章：トラップとシステムコール（`trap.tex`）

> 和訳とのコード・記述のズレの詳細は **[第4章 和訳とコードの差分メモ](books/trap-diff.md)** を参照してください。

| MIT 最新版（Ch.4 *Traps and system calls*） | 菅原訳（第4章「トラップとデバイスドライバ」） | 本リポジトリの教材 | 備考 |
| --- | --- | --- | --- |
| 4.1 RISC-V trap machinery | 4.1 RISC-V のトラップ機構 | [**第4章（1）アプリからOSに処理を頼む**](ch04-syscall.md) | |
| 4.2 Traps from user space | 4.3 ユーザ空間からのトラップ | [**第4章（1）アプリからOSに処理を頼む**](ch04-syscall.md) | **和訳 4.2 と 4.3 の順序が入れ替わり**、`prepare_return` + `return satp` 方式へ変更 |
| 4.3 Code: Calling system calls | 4.5 Code: システムコールを呼ぶ | [**第4章（1）アプリからOSに処理を頼む**](ch04-syscall.md) | 例題が `initcode.S` の `exec` からシェルの `write`（`usys.S`）へ変更 |
| 4.4 Code: System call arguments | 4.6 Code: システムコールの引数 | [**第4章（1）アプリからOSに処理を頼む**](ch04-syscall.md)（`argint` 等／`copyin` 詳細は今後追加） | `copyin` / `copyinstr` に `psz` 引数と `vmfault` 呼び出しが追加 |
| 4.5 Traps from kernel space | 4.2 カーネル空間からのトラップ | 未作成 | **和訳 4.2 から 4.5 へ後ろに移動** |
| 4.6 Real world | 4.9 世の中のオペレーティングシステム（前半） | 未作成 | 和訳 4.9 の後半（割込・ドライバ・DMA・ポーリング）は Ch.6 の 6.5 へ移動 |
| 4.7 Exercises | —（和訳 4.10 は Ch.6 の 6.6 へ移動） | 未作成 | `trampoline.S` / `TRAPFRAME` / `TRAMPOLINE` に関する新しい練習問題3問 |

### 第5章：ページフォルト（`pgfault.tex`）

| MIT 最新版（Ch.5 *Page faults*） | 菅原訳 | 本リポジトリの教材 | 備考 |
| --- | --- | --- | --- |
| 5.1 Lazy allocation | —（章自体なし） | 未作成 | **最新版で新設された章** |
| 5.2 Code | —（旧 3.7 `Code: sbrk` を発展） | 未作成 | `sys_sbrk`（`SBRK_LAZY` / `SBRK_EAGER`）と `vmfault` を解説 |
| 5.3 Real world: Copy-On-Write (COW) fork | — | 未作成 | **新設** |
| 5.4 Real world: Demand paging | — | 未作成 | **新設** |
| 5.5 Real world: Memory-mapped files | — | 未作成 | **新設** |
| 5.6 Exercises | — | 未作成 | **新設** |

### 第6章：割り込みとデバイスドライバ（`interrupt.tex`）

| MIT 最新版（Ch.6 *Interrupts and device drivers*） | 菅原訳（第4章「トラップとデバイスドライバ」後半） | 本リポジトリの教材 | 備考 |
| --- | --- | --- | --- |
| （章冒頭：ドライバの概要・`devintr`・top/bottom half） | 4.7 デバイスドライバ | 未作成 | **和訳 第4章から独立章として分離** |
| 6.1 Code: Console input | 4.8 Code: コンソールドライバ | 未作成 | 入力側（`consoleread` / `uartintr` / `consoleintr`）に整理 |
| 6.2 Code: Console output | —（対応する節なし） | 未作成 | **新設**（送信割込と `sleep` を使う `consolewrite` / `uartwrite`） |
| 6.3 Concurrency in drivers | —（4.8 末尾の記述を拡充して独立節化） | 未作成 | **新設** |
| 6.4 Timer interrupts | 4.4 タイマ割込 | 未作成 | **4.4 から移動**。M-mode `CLINT` + `timervec` 方式から S-mode `stimecmp` / `clockintr` 方式へ全面刷新 |
| 6.5 Real world | 4.9 世の中のオペレーティングシステム（後半） | 未作成 | `ioctl` とリアルタイム OS の議論が追加 |
| 6.6 Exercises | 4.10 練習問題 | 未作成 | 問1が出力の割込化から「割込を使わない実装への変更」に反転 |

### 第7章：ロック（`lock.tex`）

| MIT 最新版（Ch.7 *Locking*） | 菅原訳（第5章「ロック」） | 本リポジトリの教材 | 備考 |
| --- | --- | --- | --- |
| 7.1 Races | 5.1 競合状態 | 未作成 | 章番号 5 → 7 |
| 7.2 Code: Locks | 5.2 Code: ロック | 未作成 | |
| 7.3 Code: Using locks | 5.3 Code: ロックを使う | 未作成 | |
| 7.4 Deadlock and lock ordering | 5.4 デッドロックとロック順序 | 未作成 | |
| 7.5 Locks and interrupts | 5.5 ロックと割込ハンドラ | 未作成 | |
| 7.6 Instruction and memory ordering | 5.6 命令とメモリの順序 | 未作成 | |
| 7.7 Programming with Atomics | —（対応する節なし） | 未作成 | **最新版で新設** |
| 7.8 Sleep locks | 5.7 スリープロック | 未作成 | 節番号 5.7 → 7.8 |
| 7.9 Real world | 5.8 世の中のオペレーティングシステム | 未作成 | 節番号 5.8 → 7.9 |
| 7.10 Exercises | 5.9 練習問題 | 未作成 | 節番号 5.9 → 7.10 |

### 第8章：スケジューリング（`sched.tex`）

| MIT 最新版（Ch.8 *Scheduling*） | 菅原訳（第6章「スケジューリング」前半） | 本リポジトリの教材 | 備考 |
| --- | --- | --- | --- |
| 8.1 Multiplexing | 6.1 マルチプレクス | 未作成 | 和訳 第6章の前半が Ch.8 に（章番号 6 → 8） |
| 8.2 Context switch overview | —（6.1〜6.2 内の説明が独立節化） | 未作成 | **独立節として新設** |
| 8.3 Code: Context switching | 6.2 Code: コンテキストスイッチ | 未作成 | 節番号 6.2 → 8.3 |
| 8.4 Code: Scheduling | 6.3 Code: スケジューリング | 未作成 | 節番号 6.3 → 8.4 |
| 8.5 Code: mycpu and myproc | 6.4 Code: `mycpu` と `myproc` | 未作成 | 節番号 6.4 → 8.5 |
| 8.6 Real world | 6.9 世の中のオペレーティングシステム（前半） | 未作成 | スケジューリングに関する部分 |
| 8.7 Exercises | 6.10 練習問題（一部） | 未作成 | |

### 第9章：Sleep と Wakeup（`sleep.tex`）

| MIT 最新版（Ch.9 *Sleep and Wakeup*） | 菅原訳（第6章「スケジューリング」後半） | 本リポジトリの教材 | 備考 |
| --- | --- | --- | --- |
| 9.1 Overview | 6.5 `sleep` と `wakeup` | 未作成 | **和訳 第6章の後半が独立章として分離** |
| 9.2 Code: Sleep and wakeup | 6.6 Code: Sleep と wakeup | 未作成 | 最新コードでは `sleep_prepare` + `sleep` 方式へ変更 |
| 9.3 Code: Pipes | 6.7 Code: パイプ | 未作成 | |
| 9.4 Code: Wait, exit, and kill | 6.8 Code: `wait`, `exit`, および `kill` | 未作成 | 関数名は `kwait` / `kexit` / `kkill` に変更 |
| 9.5 Process Locking | —（対応する節なし） | 未作成 | **最新版で新設** |
| 9.6 Real world | 6.9 世の中のオペレーティングシステム（後半） | 未作成 | セマフォ等の同期プリミティブに関する部分 |
| 9.7 Exercises | 6.10 練習問題（一部） | 未作成 | |

### 第10章：ファイルシステム（`fs.tex`）

| MIT 最新版（Ch.10 *File system*） | 菅原訳（第7章「ファイルシステム」のロギング以外） | 本リポジトリの教材 | 備考 |
| --- | --- | --- | --- |
| 10.1 Overview | 7.1 概要 | 未作成 | 章番号 7 → 10 |
| 10.2 Buffer cache layer | 7.2 バッファキャッシュ層 | 未作成 | |
| 10.3 Code: Buffer cache | 7.3 Code: バッファキャッシュ | 未作成 | ※和訳の 7.4〜7.6（ロギング）は Ch.11 へ分離 |
| 10.4 Code: Block allocator | 7.7 Code: ブロックアロケータ | 未作成 | 節番号 7.7 → 10.4 |
| 10.5 Inode layer | 7.8 inode 層 | 未作成 | 節番号 7.8 → 10.5 |
| 10.6 Code: Inodes | 7.9 Code: inode | 未作成 | 節番号 7.9 → 10.6 |
| 10.7 Code: Inode content | 7.10 Code: inode の中身 | 未作成 | 節番号 7.10 → 10.7 |
| 10.8 Code: Directory layer | 7.11 Code: ディレクトリ層 | 未作成 | 節番号 7.11 → 10.8 |
| 10.9 Code: Path names | 7.12 Code: パス名 | 未作成 | 節番号 7.12 → 10.9 |
| 10.10 File descriptor layer | 7.13 ファイルディスクリプタ層 | 未作成 | 節番号 7.13 → 10.10 |
| 10.11 Code: System calls | 7.14 Code: システムコール | 未作成 | 節番号 7.14 → 10.11 |
| 10.12 Real world | 7.15 世の中のオペレーティングシステム（ロギング以外） | 未作成 | 節番号 7.15 → 10.12 |
| 10.13 Exercises | 7.16 練習問題（ロギング以外） | 未作成 | 節番号 7.16 → 10.13 |

### 第11章：ロギング（`log.tex`）

| MIT 最新版（Ch.11 *Logging*） | 菅原訳（第7章「ファイルシステム」7.4〜7.6節） | 本リポジトリの教材 | 備考 |
| --- | --- | --- | --- |
| （章冒頭：クラッシュ回復とロギングの導入） | 7.4 ロギング層 | 未作成 | **和訳 第7章の途中（7.4〜7.6節）が独立章として分離** |
| 11.1 Log design | 7.5 ログの設計 | 未作成 | |
| 11.2 Code: Logging | 7.6 Code: ロギング | 未作成 | |
| 11.3 Real world | 7.15 世の中のオペレーティングシステム（ロギング部分） | 未作成 | |
| 11.4 Exercises | 7.16 練習問題（ロギング部分） | 未作成 | |

### 第12章：並行性・再び（`lock2.tex`）

| MIT 最新版（Ch.12 *Concurrency revisited*） | 菅原訳（第8章「並行性・再び」） | 本リポジトリの教材 | 備考 |
| --- | --- | --- | --- |
| 12.1 Locking patterns | 8.1 ロックのパターン | 未作成 | 章番号 8 → 12（節番号は 1〜5 で同一） |
| 12.2 Lock-like patterns | 8.2 ロック的なパターン | 未作成 | |
| 12.3 No locks at all | 8.3 ロックしない | 未作成 | |
| 12.4 Parallelism | 8.4 並列性 | 未作成 | |
| 12.5 Exercises | 8.5 練習問題 | 未作成 | |

### 第13章：まとめ（`sum.tex`）

| MIT 最新版（Ch.13 *Summary*） | 菅原訳（第9章「まとめ」） | 本リポジトリの教材 | 備考 |
| --- | --- | --- | --- |
| （節なし） | （節なし） | — | 章番号 9 → 13 |

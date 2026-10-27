# 『真夜中のカーネル放送室』シリーズ全体構成表（全27回）

- **番組名**: 『真夜中のカーネル放送室』（パーソナリティ：水谷なつめ）
- **対象原典（MIT 最新版）**: `books/mit-en/`（`mit-pdos/xv6-riscv-book` コミット `fa3b46bc4386fcd2c2a042f3dc850c497948b6d6`、全13章＋序文）
- **対照する和訳**: `books/sugawara-ja/`（菅原研究室訳 `de6c710ac79883a2bc68a9b9f70c1fc22de48d39`、2019年版原文 `ca13de46` ベース、全9章＋序文）
- **対象ソースコード**: `xv6-riscv/`（`mit-pdos/xv6-riscv` コミット `e93dabeb98431235c6e1a101cb96c73c923fdbc4`）
- **1回あたりの尺と文字数目安**: **約20分**（発話本文 **6,000〜6,600字**、315字/分換算で発話 19分03秒〜20分57秒 ＋ ジングル・シンキングタイム等の演出秒数 15〜25秒）
- **総回数**: **全27回**（約9時間で MIT 教科書の全章・全節を耳で完走）

---

## 1. シリーズ設計の基本方針

### 1.1 20分番組の定番コーナー構成（全回共通・7部構成）

1. **オープニング**（約1分／300〜350字）：深夜0時の挨拶、前回からの繋がり、今夜のテーマ宣言
2. **お便りコーナー**（約1分30秒〜2分／500〜650字）：初学者がつまずく疑問や「和訳と今のコードのズレ」を架空のお便りとして導入（メタ情報に架空である旨を明記）
3. **メイン前半**（約6〜7分／1,900〜2,200字）：中心概念の1つ目（なぜ必要か → 比喩と実際との違い → 仕組み・最小限のコード）
4. **ひと息コーナー**（約1分〜1分30秒／350〜450字）：前半の30秒おさらいと、深夜ラジオらしい短い小話・視点の切り替え
5. **メイン後半**（約6〜7分／1,900〜2,200字）：中心概念の2つ目（またはコードの核心・和訳との差分回収・*Real world* の視野拡大）
6. **真夜中のミニクイズコーナー**（約2分／600〜700字）：耳だけで考えて予想できる2問（各章の *Exercises* や境界条件から出題）
7. **エンディング**（約1分30秒／450〜550字）：今夜のまとめ（3点以内）、PC に戻ったときの小さな実験案内、構成表どおりの次回予告

### 1.2 序文・まとめ章・Real world・Exercises・既存試作版の扱い

- **序文（`acks.tex`）**: 第1回のオープニング〜メイン前半冒頭に組み込む。Unix Version 6（v6）と Lions 本（ソースと解説の並読）に由来する xv6 の成り立ちを伝え、後半の謝辞人名リストは読み上げない。
- **各章の *Real world* 節**: 省略せず、各章の締めくくり回（第5章のみ 5.3〜5.5 節が中核のため独立した第12回）で必ず扱う。「xv6 が教育用に割り切った点」と「Linux 等の実用 OS がどう拡張しているか」を対比し、丸暗記でない設計感覚を養う。
- **各章の *Exercises* 節**: 問題文を逐語的に読み上げることはせず、思考実験系の問いは「ミニクイズコーナー」や本文中の予想問いかけに、実装・観察系の課題はエンディングの「PC に戻ったときの小さな実験案」に組み込む。
- **第13章 *Summary*（`sum.tex`）**: 14行（759字）の総括章であるため独立回にはせず、第12章（*Concurrency revisited*）と合わせた最終回（第27回）の後半〜エンディングでシリーズ全体の結びとして扱う。
- **既存の試作第1回（`video/ep01/`、約11分、第4章 4.1〜4.4）の位置づけ**: 本構成表では章順どおり **第9回（`ep09`：4.1〜4.3＋整数引数）** および **第10回（`ep10`：4.4 ポインタ引数〜4.7）** に番号を振り直し、7コーナー・約20分フォーマットで再構成する前提とする。

---

## 2. 原典（`books/mit-en/`）全章・全節の実測分量と回数割り振り根拠

> **計測方法**: `books/mit-en/book.tex` の `\input` 順に全14ファイルを走査し、各節（`\chapter` 導入部および `\section` 単位）の **行数**、**生文字数（改行除く全文字数）**、**コメント除去後文字数（`%` コメントを除いた文字数）**、**英単語・識別子トークン数** を実測した（総計 **8,313行 / 302,299文字**）。

### 2.1 章別の実測集計と分割回数

| 入力順 | ファイル | MIT 章題 | 実測行数 | 実測文字数 | 難易度・特徴 | 割当回数 | 担当回 |
| :---: | --- | --- | ---: | ---: | --- | :---: | --- |
| 0 | `acks.tex` | *Foreword and acknowledgments* | 39 | 2,107 | 導入・歴史背景（謝辞人名列挙を含む） | （Ch.1初回に統合） | ep01 |
| 1 | `unix.tex` | **Ch.1** *Operating system interfaces* | 1,118 | 34,513 | 全章2位の分量。プロセス・FD・パイプ・FSの4概念 | **3回** | ep01〜ep03 |
| 2 | `first.tex` | **Ch.2** *Operating system organization* | 702 | 28,814 | モード切替・カーネル構成・起動連鎖・新設 Security Model | **2回** | ep04〜ep05 |
| 3 | `mem.tex` | **Ch.3** *Page tables* | 924 | 35,300 | 耳で図解なし理解が難しい3段ページ表・`walk`・`kalloc`・`kexec` | **3回** | ep06〜ep08 |
| 4 | `trap.tex` | **Ch.4** *Traps and system calls* | 512 | 21,176 | レジスタ退避・トランポリン・ポインタ検査・カーネルトラップ | **2回** | ep09〜ep10 |
| 5 | `pgfault.tex` | **Ch.5** *Page faults* | 297 | 13,585 | **和訳なしの新設章**。遅延割当コードと COW/Demand paging/mmap | **2回** | ep11〜ep12 |
| 6 | `interrupt.tex` | **Ch.6** *Interrupts and device drivers* | 308 | 14,399 | PLIC/UART送受信割込と `stimecmp` タイマ（和訳から大刷新） | **2回** | ep13〜ep14 |
| 7 | `lock.tex` | **Ch.7** *Locking* | 996 | 36,441 | 全章2位級の分量。競合・`amoswap`・順序・割込・メモリバリア・sleeplock | **3回** | ep15〜ep17 |
| 8 | `sched.tex` | **Ch.8** *Scheduling* | 433 | 14,630 | 2段コンテキストスイッチと `swtch` をまたぐ `p->lock` 手渡し | **2回** | ep18〜ep19 |
| 9 | `sleep.tex` | **Ch.9** *Sleep and Wakeup* | 773 | 26,579 | Lost wakeup と新 `sleep_prepare`、`kexit`/`kwait`、新設 `p->lock` 規則 | **2回** | ep20〜ep21 |
| 10 | `fs.tex` | **Ch.10** *File system* | 1,620 | 49,076 | 全章最大の7層構造（bio / balloc / inode / bmap / dir / path / fd / syscall） | **4回** | ep22〜ep25 |
| 11 | `log.tex` | **Ch.11** *Logging* | 345 | 13,227 | クラッシュ回復・先行書き込みログ・グループコミット | **1回** | ep26 |
| 12 | `lock2.tex` | **Ch.12** *Concurrency revisited* | 232 | 11,693 | 全章横断の高度なロックパターン・ロックなし共有・並列性 | **1回**（Ch.13統合） | ep27 |
| 13 | `sum.tex` | **Ch.13** *Summary* | 14 | 759 | 全編の総括（本質的な数行と差し替え可能な実装、Unixの先へ） | （Ch.12回に統合） | ep27 |
| **計** | **全14ファイル** | **序文 ＋ 全13章** | **8,313** | **302,299** | **1回あたり平均 308行 / 11,196字（中心概念1〜2個）** | **全27回** | **ep01〜ep27** |

### 2.2 全節（全102ブロック）の実測値・扱い区分・割当回一覧

| ファイル | 節 | 行範囲 | 行数 | 文字数(生) | 文字数(コメント除) | 語数 | 見出し | 番組での扱い | 割当回 |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- | :---: |
| `acks.tex` | 序文 | L1–L39 | 39 | 2,107 | 2,107 | 340 | Foreword and acknowledgments | 本編導入で成り立ちを解説（謝辞人名列挙は省略） | ep01 |
| `unix.tex` | Ch.1導入 | L1–L132 | 132 | 5,230 | 5,200 | 881 | Operating system interfaces | 本編（メイン前半）で解説 | ep01 |
| `unix.tex` | 1.1 | L133–L374 | 242 | 7,758 | 7,692 | 1,310 | Processes and memory | 本編（メイン後半）で解説 | ep01 |
| `unix.tex` | 1.2 | L375–L675 | 301 | 8,285 | 8,270 | 1,407 | I/O and File descriptors | 本編（メイン前半）で解説 | ep02 |
| `unix.tex` | 1.3 | L676–L828 | 153 | 4,805 | 3,397 | 612 | Pipes | 本編（メイン後半）で解説 | ep02 |
| `unix.tex` | 1.4 | L829–L1032 | 204 | 4,902 | 4,882 | 814 | File system | 本編（メイン前半〜後半前半）で解説 | ep03 |
| `unix.tex` | 1.5 | L1033–L1107 | 75 | 3,282 | 2,639 | 430 | Real world | 本編（メイン後半）で対比解説 | ep03 |
| `unix.tex` | 1.6 | L1108–L1118 | 11 | 251 | 249 | 41 | Exercises | ep02 の実験案（パイプ往復 `pingpong`）に組込 | ep02 |
| `first.tex` | 冒頭コメント | L1–L14 | 14 | 686 | 0 | 0 | *(編集用コメントのみ)* | 非表示コメントのため対象外 | (ep04) |
| `first.tex` | Ch.2導入 | L15–L71 | 57 | 2,502 | 2,499 | 419 | Operating system organization | 本編（メイン前半）で解説 | ep04 |
| `first.tex` | 2.1 | L72–L144 | 73 | 3,175 | 3,169 | 524 | Abstracting physical resources | 本編（メイン前半）で解説 | ep04 |
| `first.tex` | 2.2 | L145–L205 | 61 | 2,780 | 2,774 | 448 | User mode, supervisor mode, and system calls | 本編（メイン前半）で解説 | ep04 |
| `first.tex` | 2.3 | L206–L306 | 101 | 4,646 | 4,643 | 752 | Kernel organization | 本編（メイン後半）で解説 | ep04 |
| `first.tex` | 2.4 | L307–L355 | 49 | 1,842 | 1,839 | 271 | Code: xv6 organization | 本編（メイン後半）で見取り図紹介 | ep04 |
| `first.tex` | 2.5 | L356–L499 | 144 | 6,177 | 6,171 | 1,079 | Process overview | 本編（メイン前半）で解説 | ep05 |
| `first.tex` | 2.6 | L500–L602 | 103 | 2,952 | 2,949 | 490 | Code: Starting xv6, the first process and system call | 本編（メイン前半〜後半）で起動追跡 | ep05 |
| `first.tex` | 2.7 | L603–L670 | 68 | 3,290 | 3,287 | 557 | Security Model | 本編（メイン後半）で解説（新設節） | ep05 |
| `first.tex` | 2.8 | L671–L685 | 15 | 496 | 490 | 79 | Real world | 本編（メイン後半末尾）でスレッド対比 | ep05 |
| `first.tex` | 2.9 | L686–L702 | 17 | 268 | 132 | 21 | Exercises | ep05 の実験案（空きメモリ取得の構想・観察）に組込 | ep05 |
| `mem.tex` | 冒頭コメント | L1–L8 | 8 | 441 | 0 | 0 | *(編集用コメントのみ)* | 非表示コメントのため対象外 | (ep06) |
| `mem.tex` | Ch.3導入 | L9–L26 | 18 | 786 | 783 | 129 | Page tables | 本編（メイン前半）で解説 | ep06 |
| `mem.tex` | 3.1 | L27–L187 | 161 | 7,229 | 7,223 | 1,278 | Paging hardware | 本編（メイン前半）で3段変換を解説 | ep06 |
| `mem.tex` | 3.2 | L188–L286 | 99 | 3,919 | 3,913 | 644 | Kernel address space | 本編（メイン後半）で直接マップと配置を解説 | ep06 |
| `mem.tex` | 3.3 | L287–L434 | 148 | 5,256 | 5,253 | 902 | Code: Creating an address space | 本編（メイン前半）で `walk` / `mappages` 解説 | ep07 |
| `mem.tex` | 3.4 | L435–L453 | 19 | 594 | 591 | 101 | Physical memory allocation | 本編（メイン後半）で解説 | ep07 |
| `mem.tex` | 3.5 | L454–L548 | 95 | 2,646 | 2,643 | 453 | Code: Physical memory allocator | 本編（メイン後半）で `kalloc` / `kfree` 解説 | ep07 |
| `mem.tex` | 3.6 | L549–L627 | 79 | 3,815 | 3,812 | 644 | Process address space | 本編（メイン前半）で解説 | ep08 |
| `mem.tex` | 3.7 | L628–L824 | 197 | 7,197 | 7,191 | 1,151 | Code: exec | 本編（メイン前半〜後半）で `kexec` 解説 | ep08 |
| `mem.tex` | 3.8 | L825–L879 | 55 | 2,293 | 2,287 | 392 | Real world | 本編（メイン後半）でスーパーページ等を解説 | ep08 |
| `mem.tex` | 3.9 | L880–L924 | 45 | 1,124 | 1,121 | 183 | Exercises | ep08 のクイズ（スーパーページ・`copyin`）に組込 | ep08 |
| `trap.tex` | Ch.4導入 | L1–L54 | 54 | 2,776 | 2,776 | 472 | Traps and system calls | 本編（メイン前半）で解説 | ep09 |
| `trap.tex` | 4.1 | L55–L139 | 85 | 3,345 | 3,345 | 597 | RISC-V trap machinery | 本編（メイン前半）で制御レジスタを解説 | ep09 |
| `trap.tex` | 4.2 | L140–L293 | 154 | 6,608 | 6,558 | 1,147 | Traps from user space | 本編（メイン後半）でトランポリン往復を解説 | ep09 |
| `trap.tex` | 4.3 | L294–L351 | 58 | 1,875 | 1,875 | 303 | Code: Calling system calls | 本編（メイン後半）で `usys.pl`〜`syscall` 解説 | ep09 |
| `trap.tex` | 4.4 | L352–L410 | 59 | 2,207 | 2,207 | 365 | Code: System call arguments | 本編（メイン前半）で `copyinstr`/`walkaddr` 解説 | ep10 |
| `trap.tex` | 4.5 | L411–L478 | 68 | 3,095 | 3,095 | 538 | Traps from kernel space | 本編（メイン後半）で `kernelvec`/`kerneltrap` 解説 | ep10 |
| `trap.tex` | 4.6 | L479–L494 | 16 | 762 | 762 | 129 | Real world | 本編（メイン後半末尾）で単一ページ表方式と比較 | ep10 |
| `trap.tex` | 4.7 | L495–L512 | 18 | 508 | 508 | 86 | Exercises | ep10 のミニクイズ（なぜ `trampoline.S` はCで書けないか等）に組込 | ep10 |
| `pgfault.tex` | Ch.5導入 | L1–L44 | 44 | 2,156 | 2,153 | 355 | Page faults | 本編（メイン前半）で3種のフォルトと `stval` 解説 | ep11 |
| `pgfault.tex` | 5.1 | L45–L85 | 41 | 2,154 | 2,154 | 369 | Lazy allocation | 本編（メイン前半）で遅延割当の利点と罠を解説 | ep11 |
| `pgfault.tex` | 5.2 | L86–L143 | 58 | 2,618 | 2,618 | 433 | Code | 本編（メイン後半）で `sys_sbrk` と `vmfault` 解説 | ep11 |
| `pgfault.tex` | 5.3 | L144–L195 | 52 | 2,667 | 2,667 | 481 | Real world: Copy-On-Write (COW) fork | 本編（メイン前半）で COW `fork` を徹底解説 | ep12 |
| `pgfault.tex` | 5.4 | L196–L252 | 57 | 2,934 | 2,934 | 519 | Real world: Demand paging | 本編（メイン後半）でデマンドページングと退避を解説 | ep12 |
| `pgfault.tex` | 5.5 | L253–L276 | 24 | 632 | 347 | 55 | Real world: Memory-mapped files | 本編（メイン後半）で `mmap` を解説 | ep12 |
| `pgfault.tex` | 5.6 | L277–L297 | 21 | 424 | 421 | 72 | Exercises | 問1を ep11 実験案（`sbrk` 観察）、問2・3を ep12 クイズに組込 | ep11, ep12 |
| `interrupt.tex` | Ch.6導入 | L1–L35 | 35 | 1,581 | 1,581 | 265 | Interrupts and device drivers | 本編（メイン前半）で top/bottom half と `devintr` 解説 | ep13 |
| `interrupt.tex` | 6.1 | L36–L134 | 99 | 4,681 | 4,681 | 805 | Code: Console input | 本編（メイン前半）でキー入力〜`consoleread` 解説 | ep13 |
| `interrupt.tex` | 6.2 | L135–L161 | 27 | 1,041 | 1,041 | 177 | Code: Console output | 本編（メイン後半）で送信割込 `uartwrite` 解説 | ep13 |
| `interrupt.tex` | 6.3 | L162–L186 | 25 | 1,275 | 1,275 | 216 | Concurrency in drivers | 本編（メイン後半）で生産者・消費者並行性を解説 | ep13 |
| `interrupt.tex` | 6.4 | L187–L233 | 47 | 2,092 | 2,092 | 361 | Timer interrupts | 本編（メイン前半）で `stimecmp` と `clockintr` 解説 | ep14 |
| `interrupt.tex` | 6.5 | L234–L298 | 65 | 3,536 | 3,536 | 602 | Real world | 本編（メイン後半）でポーリング・DMA・`ioctl` 解説 | ep14 |
| `interrupt.tex` | 6.6 | L299–L308 | 10 | 193 | 193 | 35 | Exercises | 問1（`uart.c` 非割込化）を ep13 クイズ・実験案に組込 | ep13, ep14 |
| `lock.tex` | Ch.7導入 | L1–L81 | 81 | 3,135 | 2,500 | 401 | Locking | 本編（メイン前半）で並列実行と競合の導入 | ep15 |
| `lock.tex` | 7.1 | L82–L291 | 210 | 6,921 | 6,915 | 1,129 | Races | 本編（メイン前半）で `kfree` リスト破壊と不変条件を解説 | ep15 |
| `lock.tex` | 7.2 | L292–L411 | 120 | 3,666 | 3,660 | 581 | Code: Locks | 本編（メイン後半）で `amoswap` と `acquire`/`release` 解説 | ep15 |
| `lock.tex` | 7.3 | L412–L510 | 99 | 4,313 | 4,307 | 723 | Code: Using locks | 本編（メイン前半）でロック範囲と粗粒度/細粒度を解説 | ep16 |
| `lock.tex` | 7.4 | L511–L606 | 96 | 4,171 | 4,168 | 746 | Deadlock and lock ordering | 本編（メイン前半〜後半）でデッドロックと順序規則を解説 | ep16 |
| `lock.tex` | 7.5 | L607–L701 | 95 | 2,674 | 2,668 | 409 | Locks and interrupts | 本編（メイン後半）で割込デッドロックと `push_off` 解説 | ep16 |
| `lock.tex` | 7.6 | L702–L794 | 93 | 3,494 | 3,491 | 573 | Instruction and memory ordering | 本編（メイン前半）で順序逆転とメモリバリアを解説 | ep17 |
| `lock.tex` | 7.7 | L795–L814 | 20 | 956 | 953 | 148 | Programming with Atomics | 本編（メイン前半末尾）でアトミック加算（新設節）を解説 | ep17 |
| `lock.tex` | 7.8 | L815–L882 | 68 | 2,543 | 2,106 | 358 | Sleep locks | 本編（メイン後半）で `sleeplock` の必要性と制約を解説 | ep17 |
| `lock.tex` | 7.9 | L883–L930 | 48 | 2,420 | 2,414 | 413 | Real world | 本編（メイン後半）でレース検出器やロック隠蔽を解説 | ep17 |
| `lock.tex` | 7.10 | L931–L996 | 66 | 2,148 | 1,587 | 269 | Exercises | 再入可能ロックの罠・`push_off` 実験等を ep16/ep17 クイズに組込 | ep16, ep17 |
| `sched.tex` | 冒頭コメント | L1–L3 | 3 | 45 | 0 | 0 | *(編集用コメントのみ)* | 非表示コメントのため対象外 | (ep18) |
| `sched.tex` | Ch.8導入 | L4–L25 | 22 | 716 | 713 | 117 | Scheduling | 本編（メイン前半）でタイムシェアの導入 | ep18 |
| `sched.tex` | 8.1 | L26–L55 | 30 | 1,249 | 1,243 | 215 | Multiplexing | 本編（メイン前半）でCPU多重化の契機を解説 | ep18 |
| `sched.tex` | 8.2 | L56–L84 | 29 | 1,174 | 1,168 | 201 | Context switch overview | 本編（メイン前半）でスケジューラスレッド経由の理由を解説 | ep18 |
| `sched.tex` | 8.3 | L85–L163 | 79 | 3,202 | 3,127 | 567 | Code: Context switching | 本編（メイン後半）で `struct context` と `swtch` を解説 | ep18 |
| `sched.tex` | 8.4 | L164–L321 | 158 | 4,482 | 4,453 | 747 | Code: Scheduling | 本編（メイン前半）で `yield`→`scheduler` と `p->lock` 手渡し解説 | ep19 |
| `sched.tex` | 8.5 | L322–L406 | 85 | 2,750 | 2,744 | 466 | Code: mycpu and myproc | 本編（メイン後半）で `tp` レジスタと割込禁止の理由を解説 | ep19 |
| `sched.tex` | 8.6 | L407–L420 | 14 | 563 | 557 | 85 | Real world | 本編（メイン後半末尾）で優先度・省電力スケジューリングを解説 | ep19 |
| `sched.tex` | 8.7 | L421–L433 | 13 | 449 | 446 | 70 | Exercises | `swtch` が caller-saved を保存しない理由等を ep18/ep19 クイズに組込 | ep18, ep19 |
| `sleep.tex` | Ch.9導入 | L1–L33 | 33 | 1,151 | 1,148 | 194 | Sleep and Wakeup | 本編（メイン前半）で条件待機の導入 | ep20 |
| `sleep.tex` | 9.1 | L34–L146 | 113 | 4,671 | 4,668 | 738 | Overview | 本編（メイン前半）で lost wakeup 問題の本質を段階解説 | ep20 |
| `sleep.tex` | 9.2 | L147–L213 | 67 | 3,159 | 3,153 | 517 | Code: Sleep and wakeup | 本編（メイン後半）で `sleep_prepare`＋`sleep` と偽起床を解説 | ep20 |
| `sleep.tex` | 9.3 | L214–L359 | 146 | 3,574 | 3,566 | 579 | Code: Pipes | 本編（メイン後半）で `pipewrite` / `piperead` の待機を解説 | ep20 |
| `sleep.tex` | 9.4 | L360–L532 | 173 | 5,828 | 5,825 | 1,006 | Code: Wait, exit, and kill | 本編（メイン前半）で `ZOMBIE`・孤児引取・協調的 `kkill` を解説 | ep21 |
| `sleep.tex` | 9.5 | L533–L620 | 88 | 3,463 | 2,707 | 457 | Process Locking | 本編（メイン後半）で `p->lock` 9つの役割と `wait_lock` を解説 | ep21 |
| `sleep.tex` | 9.6 | L621–L737 | 117 | 3,583 | 3,577 | 632 | Real world | 本編（メイン後半）でセマフォ・たらい回し起床・強制 kill を解説 | ep21 |
| `sleep.tex` | 9.7 | L738–L773 | 36 | 1,150 | 850 | 146 | Exercises | `kill` された睡眠中プロセスの挙動等を ep21 クイズに組込 | ep21 |
| `fs.tex` | Ch.10導入 | L1–L51 | 51 | 1,807 | 1,439 | 251 | File system | 本編（メイン前半）で永続化とクラッシュ耐性の課題を提示 | ep22 |
| `fs.tex` | 10.1 | L52–L155 | 104 | 3,973 | 3,964 | 707 | Overview | 本編（メイン前半）で7層構造とディスク区画配置を解説 | ep22 |
| `fs.tex` | 10.2 | L156–L211 | 56 | 2,156 | 2,103 | 379 | Buffer cache layer | 本編（メイン後半）でキャッシュと排他の2つの役割を解説 | ep22 |
| `fs.tex` | 10.3 | L212–L367 | 156 | 4,542 | 4,533 | 784 | Code: Buffer cache | 本編（メイン後半）で `bget`/`bread`/`brelse` と LRU を解説 | ep22 |
| `fs.tex` | 10.4 | L368–L426 | 59 | 1,713 | 1,660 | 297 | Code: Block allocator | 本編（メイン後半末尾）でビットマップ `balloc`/`bfree` を解説 | ep22 |
| `fs.tex` | 10.5 | L427–L569 | 143 | 4,536 | 4,483 | 801 | Inode layer | 本編（メイン前半）で `dinode` と `inode`、`ref` と `nlink` を解説 | ep23 |
| `fs.tex` | 10.6 | L570–L730 | 161 | 5,504 | 5,504 | 998 | Code: Inodes | 本編（メイン前半〜後半）で `iget`/`ilock`/`iput`/`ireclaim` 解説 | ep23 |
| `fs.tex` | 10.7 | L731–L904 | 174 | 4,746 | 4,257 | 708 | Code: Inode content | 本編（メイン後半）で直接・間接ブロック `bmap` と `readi`/`writei` 解説 | ep23 |
| `fs.tex` | 10.8 | L905–L1006 | 102 | 3,134 | 3,125 | 541 | Code: Directory layer | 本編（メイン前半）で `dirent`・`dirlookup`・`dirlink` を解説 | ep24 |
| `fs.tex` | 10.9 | L1007–L1136 | 130 | 3,784 | 3,775 | 610 | Code: Path names | 本編（メイン前半〜後半）で `namex` の段階的ロック探索を解説 | ep24 |
| `fs.tex` | 10.10 | L1137–L1258 | 122 | 3,249 | 3,240 | 528 | File descriptor layer | 本編（メイン後半）で `struct file` とオープンファイル表を解説 | ep24 |
| `fs.tex` | 10.11 | L1259–L1459 | 201 | 5,277 | 5,224 | 839 | Code: System calls | 本編（メイン前半）で `sys_link`/`sys_unlink`/`create`/`sys_open` 解説 | ep25 |
| `fs.tex` | 10.12 | L1460–L1530 | 71 | 3,124 | 3,071 | 523 | Real world | 本編（メイン後半）で現代のバッファキャッシュ・B木ディレクトリ等を解説 | ep25 |
| `fs.tex` | 10.13 | L1531–L1620 | 90 | 1,531 | 1,531 | 247 | Exercises | `balloc` パニック理由・孤児 inode・シンボリックリンク等を ep22〜25 クイズに組込 | ep22〜ep25 |
| `log.tex` | Ch.11導入 | L1–L76 | 76 | 3,404 | 3,209 | 591 | Logging | 本編（メイン前半）で停電・クラッシュ時の不整合シナリオを解説 | ep26 |
| `log.tex` | 11.1 | L77–L160 | 84 | 3,571 | 3,562 | 630 | Log design | 本編（メイン前半）でログヘッダ・コミット点・グループコミットを解説 | ep26 |
| `log.tex` | 11.2 | L161–L288 | 128 | 4,254 | 4,195 | 690 | Code: Logging | 本編（メイン後半）で `begin_op`/`log_write`/`end_op`/`recover_from_log` 解説 | ep26 |
| `log.tex` | 11.3 | L289–L312 | 24 | 962 | 912 | 159 | Real world | 本編（メイン後半末尾）で xv6 ログの非効率性と現代ジャーナリングを比較 | ep26 |
| `log.tex` | 11.4 | L313–L345 | 33 | 1,036 | 992 | 165 | Exercises | `log_write` への `printk` 1行追加観察を ep26 の実験案にそのまま採用 | ep26 |
| `lock2.tex` | Ch.12導入 | L1–L13 | 13 | 427 | 427 | 66 | Concurrency revisited | 本編（メイン前半）で正しさ・並列性・明快さの三すくみを導入 | ep27 |
| `lock2.tex` | 12.1 | L14–L100 | 87 | 4,394 | 4,157 | 745 | Locking patterns | 本編（メイン前半）で2段ロック・スレッド横断ロック・参照数を解説 | ep27 |
| `lock2.tex` | 12.2 | L101–L149 | 49 | 2,638 | 2,638 | 476 | Lock-like patterns | 本編（メイン前半）で `namex` 参照数と物理ページの所有権移転を解説 | ep27 |
| `lock2.tex` | 12.3 | L150–L174 | 25 | 1,352 | 1,352 | 237 | No locks at all | 本編（メイン後半）で `volatile started` と暗黙のメモリバリアを解説 | ep27 |
| `lock2.tex` | 12.4 | L175–L219 | 45 | 2,499 | 2,499 | 437 | Parallelism | 本編（メイン後半）で `pipe`・`scheduler`・`fork` の並列性を解説 | ep27 |
| `lock2.tex` | 12.5 | L220–L232 | 13 | 383 | 383 | 63 | Exercises | パイプ読み書き同時並列化のアイデアを ep27 ミニクイズに組込 | ep27 |
| `sum.tex` | Ch.13全体 | L1–L14 | 14 | 759 | 759 | 124 | Summary | 本編（メイン後半結び〜エンディング）で全27回の総括として解説 | ep27 |

---

## 3. 全27回 回別詳細構成

### 第1回（`ep01`）：シェルはカーネルじゃない？ ― 分身する `fork` と入れ替わる `exec`
- **対応する MIT の章・節**: 序文（`acks.tex`）＋ Ch.1 *Operating system interfaces* 導入部・1.1 *Processes and memory*（計 413行 / 15,095字）
- **対応する和訳の章・節**: 序文と謝辞（`acks.tex`）＋ 第1章「オペレーティングシステムのインタフェース」導入部・1.1「プロセスとメモリ」
- **前提となる回**: なし（シリーズ初回）
- **中心概念（2個）**: ① カーネル・プロセス・システムコールの関係と「シェルは普通のユーザープログラムである」こと、② プロセスの分身を作る `fork` と中身を別プログラムに入れ替える `exec`（および `exit` / `wait` の連携）
- **中心の問い**: 「コマンドを受け付けるシェルは OS 本体の一部なの？ そして新しいコマンドを動かすとき、なぜ1発で起動せず『自分の分身（`fork`）』を作ってから『中身を入れ替える（`exec`）』という回りくどい2段階を踏むの？」
- **主に触れるコード**: `user/sh.c`（`main`, `getcmd`, `fork1`, `runcmd`）、`user/echo.c`（`main`）、`kernel/syscall.h`（`SYS_fork`, `SYS_pause`, `SYS_sync` 等の番号定義）、`user/user.h`（システムコール宣言一覧）
- **PC に戻ったときの小さな実験案**: `./scripts/run` で QEMU 上の xv6 を起動し、シェル上で `sh` の中からさらに `sh` を起動して `Ctrl-P` でプロセス一覧に2つの `sh` が並ぶのを確認し、続けて `Ctrl-D`（EOF）で1段抜けても元の親シェルが生きていること（「シェルも普通の1プロセスにすぎない」こと）を確かめる（終了は `Ctrl-a` → `x`）。
- **和訳と今のコードのズレで触れるべき点**: ① 和訳のシステムコール一覧表（図1.2）にある一時停止の `sleep(n)` は、カーネル内部の `sleep` 関数との混同を避けるため、現在のコードと MIT 最新版では **`pause(n)`（`SYS_pause`）に改名**されたこと、② 和訳の表には無かった **`uptime()` と `sync()` を含め現在は全22個のシステムコール**があること（また `fstat` も実際は2引数であること）、③ 序文の MIT 講義番号が `6.828` に加え `6.1810` になったこと。

---

### 第2回（`ep02`）：0番・1番・2番の正体 ― ファイル記述子とパイプの魔法
- **対応する MIT の章・節**: Ch.1 1.2 *I/O and File descriptors*・1.3 *Pipes*・1.6 *Exercises*（計 465行 / 13,341字）
- **対応する和訳の章・節**: 第1章 1.2「I/O とファイルディスクリプタ」・1.3「パイプ」・1.6「練習問題」
- **前提となる回**: 第1回（`fork`・`exec`・`wait` の基本動作）
- **中心概念（2個）**: ① ファイル・画面・パイプを同じ整数番号で扱う「ファイル記述子」と I/O リダイレクト（`fork` と `exec` が分離されている理由の答え合わせ）、② カーネル内バッファでプロセス同士をつなぐ「パイプ」と書き込み端クローズの重要性
- **中心の問い**: 「`cat < input.txt` や `echo hi | wc` と打ったとき、`cat` や `wc` 自身のコードはファイルを一切開いていないのに、どうして勝手に入力先や出力先が切り替わるの？」
- **主に触れるコード**: `user/cat.c`（`cat`, `main`）、`user/wc.c`（`wc`, `main`）、`user/sh.c`（`main` のコンソール記述子確保、`runcmd` の `REDIR` 分岐・`PIPE` 分岐）、`kernel/fcntl.h`（`O_RDONLY`, `O_WRONLY`, `O_RDWR`, `O_CREATE`, `O_TRUNC`）
- **PC に戻ったときの小さな実験案**: xv6 シェルで `echo hello world > a`、`cat < a | wc` を実行してリダイレクトとパイプを体感したあと、第1章 1.6 練習問題にならい「2本のパイプで親子プロセス間に1バイトを往復させる `pingpong`」の動きを紙や実験ブランチ（`./scripts/exp pingpong`）で書いてみる。
- **和訳と今のコードのズレで触れるべき点**: 和訳 1.2節には無かった `open` フラグの解説が MIT 最新版で拡充され、ファイルの中身を長さ0に切り詰める **`O_TRUNC`（`kernel/fcntl.h`）** が追加されている点。

---

### 第3回（`ep03`）：ファイル名と実体は別物？ ― `inode` とリンク、そして `cd` の秘密
- **対応する MIT の章・節**: Ch.1 1.4 *File system*・1.5 *Real world*（計 279行 / 8,184字）
- **対応する和訳の章・節**: 第1章 1.4「ファイルシステム」・1.5「世の中のオペレーティングシステム」（および和訳 1.1 末尾にあった root 権限の記述）
- **前提となる回**: 第1回・第2回
- **中心概念（2個）**: ① ファイルの「名前（ディレクトリ内のリンク）」と「実体（`inode`）」の分離（`link` と `unlink` の仕組み）、② なぜ `mkdir` や `rm` は外部プログラムなのに `cd` だけはシェル自身に組み込まれているのか（＋POSIX や Plan 9 との比較）
- **中心の問い**: 「同じファイルに2つの名前を付けたり、開いている最中のファイルを `unlink` で消したりすると中身はどうなるの？ また、どうして `user/` の中に `cd.c` というファイルだけは存在しないの？」
- **主に触れるコード**: `kernel/stat.h`（`struct stat`）、`user/sh.c`（`main` 内の `cd` 判定と `chdir` 呼び出し）、`user/ls.c`（`ls`）、`user/ln.c`（`main`）、`user/rm.c`（`main`）、`user/mkdir.c`（`main`）
- **PC に戻ったときの小さな実験案**: xv6 シェルで `echo night > a` → `ln a b` → `ls` を実行し、`a` と `b` の `inode` 番号が同じでサイズがともに 6 バイトであること、続いて `rm a` しても `cat b` で中身が読めることを観察する。
- **和訳と今のコードのズレで触れるべき点**: ① `user/sh.c` の `cd` 判定が、和訳の `buf[0] == 'c'` から、先頭の空白・タブを読み飛ばした **`cmd[0] == 'c'`** に改良されている点、② 和訳 1.1節末尾にあった「xv6 の全プロセスは root として動く」という説明が MIT 最新版では 1.5 *Real world* に整理された点。

---

### 第4回（`ep04`）：なぜカーネルは特権で守られるのか ― 3つのCPUモードとOSの設計図
- **対応する MIT の章・節**: Ch.2 *Operating system organization* 導入部・2.1 *Abstracting physical resources*・2.2 *User mode, supervisor mode, and system calls*・2.3 *Kernel organization*・2.4 *Code: xv6 organization*（計 355行 / 15,631字）
- **対応する和訳の章・節**: 第2章「オペレーティングシステムの構成」導入部・2.1〜2.4
- **前提となる回**: 第1回（システムコールの概念）
- **中心概念（2個）**: ① 隔離（isolation）を実現する RISC-V の3つの特権モード（マシン・スーパーバイザー・ユーザー）とハードウェア資源の抽象化、② モノリシックカーネルとマイクロカーネルの設計トレードオフ（および `kernel/` 全ファイルの役割マップ）
- **中心の問い**: 「プログラムがバグや悪意で他のプロセスのメモリを書き換えようとしたとき、誰がどうやって止めているの？ そして OS の機能を全部カーネルに入れるのと、外に出すのとでは何が違うの？」
- **主に触れるコード**: `kernel/riscv.h`（`MSTATUS_MPP_S`, `SSTATUS_SPP`, `PTE_U`）、`kernel/memlayout.h`（`KERNBASE`, `PHYSTOP`）、`kernel/param.h`（`NPROC`, `NCPU`）、`kernel/defs.h`（サブシステム間の関数宣言一覧）
- **PC に戻ったときの小さな実験案**: `xv6-riscv/kernel/` のファイル一覧と `kernel/defs.h` の見出しコメントを眺め、第1章で触った `fork`・`pipe`・`open` が `proc.c`・`pipe.c`・`sysfile.c` のどこに住んでいるか宝探しをする。
- **和訳と今のコードのズレで触れるべき点**: 2.4節のカーネル構成ファイル一覧において、和訳の `kernel/printf.c`（カーネル内 `printf`）はユーザーの `printf` と区別するため **`kernel/printk.c`（`printk` 関数）へ改名**されている点。

---

### 第5回（`ep05`）：電源オンから最初のプロセス `/init` まで ― 消えた `initcode.S` とセキュリティモデル
- **対応する MIT の章・節**: Ch.2 2.5 *Process overview*・2.6 *Code: Starting xv6, the first process and system call*・2.7 *Security Model*・2.8 *Real world*・2.9 *Exercises*（計 347行 / 13,183字）
- **対応する和訳の章・節**: 第2章 2.5「プロセスの概要」・2.6「Code: xv6 の起動と最初のプロセス」・2.7「世の中のオペレーティングシステム」・2.8「練習問題」（※MIT 2.7 *Security Model* は **和訳なし**）
- **前提となる回**: 第1回・第4回
- **中心概念（2個）**: ① プロセスの管理簿（`struct proc`、ユーザー/カーネル2つのスタック）と電源投入（`_entry` → `start` → `main` → `userinit` → `forkret` → `/init`）の起動リレー、② ユーザーコードを「悪意がある前提」で封じ込め、カーネル自身の不整合には `panic` で停止するセキュリティモデル
- **中心の問い**: 「まだプロセスが1つも存在しない電源オン直後の真っ白な状態から、どうやって最初のユーザープロセス `/init` とシェルが立ち上がるの？」
- **主に触れるコード**: `kernel/proc.h`（`struct proc`）、`kernel/entry.S`（`_entry`）、`kernel/start.c`（`stack0`, `start`）、`kernel/main.c`（`main`）、`kernel/proc.c`（`userinit`, `forkret`）、`user/init.c`（`main`）、`kernel/printk.c`（`panic`）
- **PC に戻ったときの小さな実験案**: `./scripts/debug` で GDB を接続し、`main` と `userinit` にブレークポイントを張って起動直後の `entry.S` → `start` → `main` → `userinit` のバトンリレーを実際にステップ確認する。
- **和訳と今のコードのズレで触れるべき点**: ① **最大の違い**：和訳 2.6節の主役だったアセンブリ小片 **`user/initcode.S` は廃止・削除**され、現在のコードでは最初のプロセスが `forkret()`（`first == 1`）からカーネル内で直接 **`kexec("/init", ...)`** を呼んで起動する方式に刷新された点、② **MIT 2.7節 *Security Model* が新設**された点、③ `p->tf` が `p->trapframe` に改名された点。

---

### 第6回（`ep06`）：仮想アドレスという魔法の地図 ― RISC-V 3段ページテーブルとカーネル空間
- **対応する MIT の章・節**: Ch.3 *Page tables* 導入部・3.1 *Paging hardware*・3.2 *Kernel address space*（計 286行 / 12,375字）
- **対応する和訳の章・節**: 第3章「ページテーブル」導入部・3.1「ページングハードウェア」・3.2「カーネルのアドレス空間」
- **前提となる回**: 第4回・第5回
- **中心概念（2個）**: ① 39ビットの仮想アドレスを9ビット×3段の目次＋12ビットのページ内位置に分けて物理アドレスへ変換する Sv39 ハードウェアの仕組み、② カーネル自身のアドレス空間（物理メモリの直接マップ、装置レジスタ、ガードページ付きカーネルスタック）
- **中心の問い**: 「どのプロセスも 0 番地から始まるメモリを使っているのに、どうして現実の物理メモリ上でぶつからないの？ そして1枚の巨大な対応表ではなく『3段の目次』に分けるのはなぜ？」
- **主に触れるコード**: `kernel/riscv.h`（`SATP_SV39`, `MAKE_SATP`, `PTE_V`, `PTE_R`, `PTE_W`, `PTE_X`, `PTE_U`, `PA2PTE`, `PTE2PA`, `PX`）、`kernel/memlayout.h`（`UART0`, `VIRTIO0`, `PLIC`, `KERNBASE`, `PHYSTOP`, `TRAMPOLINE`, `KSTACK`）
- **PC に戻ったときの小さな実験案**: `kernel/memlayout.h` と `kernel/riscv.h` を開き、`0x80000000`（`KERNBASE`）を 4096（`0x1000`）で割ったページ番号と、`PX` マクロが9ビットずつ取り出す計算を手計算または GDB の `p/x` で確かめる。
- **和訳と今のコードのズレで触れるべき点**: 基本設計は共通だが、3.2節で触れる `fork` のカーネル内実装関数名が和訳の `fork` から **`kfork`（`kernel/proc.c`）** に改名されている点。

---

### 第7回（`ep07`）：地図を編む `walk` と、空き地を配る `kalloc` ― メモリ管理の裏方コード
- **対応する MIT の章・節**: Ch.3 3.3 *Code: Creating an address space*・3.4 *Physical memory allocation*・3.5 *Code: Physical memory allocator*（計 262行 / 8,496字）
- **対応する和訳の章・節**: 第3章 3.3「Code: アドレス空間を作る」・3.4「物理メモリのアロケート」・3.5「Code: 物理メモリのアロケータ」
- **前提となる回**: 第6回（3段ページテーブルの構造）
- **中心概念（2個）**: ① 3段の木をたどって必要に応じて途中の目次ページを作り足す `walk` と `mappages`、② 空いている 4096 バイトの物理ページ自身の先頭に「次の空きページの番地」を書き込んで数珠つなぎにする `kalloc` / `kfree`
- **中心の問い**: 「まだメモリの管理表すら作れない起動直後に、カーネルはどうやって数万枚の空き物理ページを余分なメモリゼロでリスト管理し、ページテーブルを組み立てているの？」
- **主に触れるコード**: `kernel/vm.c`（`kvminit`, `kvmmake`, `kvmmap`, `walk`, `mappages`）、`kernel/proc.c`（`proc_mapstacks`）、`kernel/kalloc.c`（`struct run`, `kinit`, `kfree`, `kalloc`）
- **PC に戻ったときの小さな実験案**: `kernel/kalloc.c` の `kfree` と `kalloc` でページの中身をそれぞれ `1` と `5`（ガラクタ値）で埋めている理由を確認し、`./scripts/debug` で `kalloc()` 呼び出し直後の `kmem.freelist` のポインタ連鎖を1つたどってみる。
- **和訳と今のコードのズレで触れるべき点**: ① 和訳 3.3節ではカーネルページテーブルの構築が `kvminit` に直書きされ、カーネルスタックのマップは `procinit` にあったが、現在のコードでは **`kvmmake` と `proc_mapstacks`（`kernel/proc.c`）** に綺麗に分離されている点。

---

### 第8回（`ep08`）：プログラムが命を吹き込まれる瞬間 ― プロセス空間と `kexec` の全工程
- **対応する MIT の章・節**: Ch.3 3.6 *Process address space*・3.7 *Code: exec*・3.8 *Real world*・3.9 *Exercises*（計 376行 / 14,429字）
- **対応する和訳の章・節**: 第3章 3.6「プロセスのアドレス空間」・3.8「Code: exec」・3.9「世の中のオペレーティングシステム」・3.10「練習問題」（※和訳 3.7 `Code: sbrk` は MIT 第5章へ発展移動）
- **前提となる回**: 第1回・第6回・第7回
- **中心概念（2個）**: ① ユーザープロセスのアドレス空間配置（命令・データ・ガードページ・スタック・ヒープ・最高番地の退避領域）、② ELF 実行ファイルを検証しながら新しいページテーブルに読み込み、失敗時は元のプロセスを傷つけず引き返す `kexec` の安全な入れ替え手順（＋スーパーページ等の現実の工夫）
- **中心の問い**: 「`exec` で壊れたファイルや大きすぎるファイルを指定したとき、すでに元のメモリを消していたら戻れなくなるはずなのに、`kexec` はどうやって安全に入れ替えているの？」
- **主に触れるコード**: `kernel/memlayout.h`（`TRAPFRAME`, `TRAMPOLINE`）、`kernel/elf.h`（`struct elfhdr`, `struct proghdr`）、`kernel/exec.c`（`kexec`, `loadseg`）、`kernel/vm.c`（`uvmalloc`, `uvmclear`, `copyout`）
- **PC に戻ったときの小さな実験案**: xv6 シェルで存在しないコマンド名やディレクトリ名（`ls` ではなく `.` など）を打ったときにシェルが壊れず `exec ... failed` と表示する動きを確かめ、`kernel/exec.c` の `bad:` ラベルへのジャンプ箇所を追ってみる。
- **和訳と今のコードのズレで触れるべき点**: ① **節の移動**：和訳にあった **3.7節 `Code: sbrk` は第3章から外れ、新設の第5章（遅延割り当て）へ発展移動**したため、3.8節以降が 3.7〜3.9節へ繰り上がっている点、② 関数名が `exec` から **`kexec`** に改名された点、③ 和訳 3.8節の「`ustack` の最初の3エントリはフェイクのリターンPC等」という x86 由来の旧記述はなくなり、現在は `a0` に `argc`、`p->trapframe->a1` に `sp` を入れ、`ustack` には純粋に `argv` ポインタ配列のみを積む点、④ ELF セグメント権限も `flags2perm` で厳密に反映される点。

---

### 第9回（`ep09`）：境界を越える往復切符 ― トランポリンと消えた `usertrapret` の謎
> ※既存の試作台本（`video/ep01/script-radio.md`、約11分）を、第3章までの知識を踏まえた20分フル版として再構成する回。
- **対応する MIT の章・節**: Ch.4 *Traps and system calls* 導入部・4.1 *RISC-V trap machinery*・4.2 *Traps from user space*・4.3 *Code: Calling system calls*（計 351行 / 14,604字）
- **対応する和訳の章・節**: 第4章「トラップとデバイスドライバ」導入部・4.1「RISC-V のトラップ機構」・4.3「ユーザ空間からのトラップ」・4.5「Code: システムコールを呼ぶ」
- **前提となる回**: 第1回・第4回・第6回・第8回
- **中心概念（2個）**: ① `ecall` 命令によるハードウェア最小動作と、両ページテーブルの最高番地に置かれた「トランポリン（`uservec` / `userret`）」および退避シート（`trapframe`）による空間切り替え、② システムコール番号表（`usys.pl` → `syscall`）から `prepare_return` と直接リターンでユーザー空間へ帰る往復路
- **中心の問い**: 「ページテーブルを切り替えた瞬間に実行中の番地まで消えてしまいそうなのに、CPU はどうやって足を踏み外さずにカーネルへ飛び込み、結果を持ってアプリの次の命令へ戻ってくるの？」
- **主に触れるコード**: `user/usys.pl`（`entry`）、`kernel/trampoline.S`（`uservec`, `userret`）、`kernel/proc.h`（`struct trapframe`）、`kernel/trap.c`（`usertrap`, `prepare_return`）、`kernel/syscall.c`（`syscall`, `syscalls`）、`kernel/syscall.h`（`SYS_write`）
- **PC に戻ったときの小さな実験案**: `./scripts/check-lab syscall-trace` を実行して `echo hi` のシステムコール呼び出しと戻り値を自動検証し、`docs/ch04-syscall.md` の5行改造パッチの中身を確認する。
- **和訳と今のコードのズレで触れるべき点**: ① 章題が「トラップとシステムコール」に変わり、**節順が「4.2 ユーザ空間 → 4.5 カーネル空間」に入れ替わった**点、② 和訳の **`usertrapret` 関数が廃止**され、`prepare_return` 設定後に `usertrap` が `satp` 値を `return` して `userret` へ直接戻る方式になった点、③ `sscratch` の使い方が `csrrw` 交換から `csrw` 一時退避＋`li a0, TRAPFRAME` に変わった点、④ 4.3節の例題が廃止済みの `initcode.S` からシェルの `write` に変わった点（詳細は `docs/books/trap-diff.md`）。

---

### 第10回（`ep10`）：悪意あるポインタを見抜け ― 引数コピーの関所とカーネル内トラップ
- **対応する MIT の章・節**: Ch.4 4.4 *Code: System call arguments*・4.5 *Traps from kernel space*・4.6 *Real world*・4.7 *Exercises*（計 161行 / 6,572字）
- **対応する和訳の章・節**: 第4章 4.6「Code: システムコールの引数」・4.2「カーネル空間からのトラップ」・4.9「世の中のオペレーティングシステム（前半）」（※MIT 4.7 練習問題は新設）
- **前提となる回**: 第7回・第9回
- **中心概念（2個）**: ① ユーザーが渡したポインタ番地をそのまま逆参照せず、ソフトウェアでユーザーのページテーブルを引いて検証・コピーする `copyin` / `copyinstr` / `walkaddr`、② カーネル実行中に割り込みや例外が起きたときの処理（`kernelvec` と `kerneltrap`）および単一ページテーブル方式との比較
- **中心の問い**: 「もし悪意あるアプリが `write` システムコールに『カーネル秘密データの番地』を渡してきたら、すでに特権モードに入っているカーネルはどうやって騙されずに防ぐの？」
- **主に触れるコード**: `kernel/syscall.c`（`argraw`, `argint`, `argaddr`, `argstr`, `fetchstr`, `fetchaddr`）、`kernel/vm.c`（`copyin`, `copyinstr`, `walkaddr`）、`kernel/kernelvec.S`（`kernelvec`）、`kernel/trap.c`（`kerneltrap`）
- **PC に戻ったときの小さな実験案**: `./scripts/test name copyin` を実行し、不正な番地をシステムコールに渡してもカーネルがクラッシュせずエラーで弾く自動テストが通ることを確かめる。
- **和訳と今のコードのズレで触れるべき点**: ① `argint` / `argaddr` の戻り値が `int` から `void` に整理された点、② `copyin` / `copyout` / `copyinstr` に第2引数 `psz` と後続章の `vmfault` 呼び出しが追加された点、③ 和訳 4.2節では「`kernelvec` は全レジスタを保存」とあるが、現在は C の規約を活かして **caller-saved レジスタのみ保存**（かつコア移動に備え `tp` は上書き復元しない）に最適化された点。

---

### 第11回（`ep11`）：使う瞬間までメモリは配らない ― ページフォルトと遅延割り当ての仕組み
- **対応する MIT の章・節**: Ch.5 *Page faults* 導入部・5.1 *Lazy allocation*・5.2 *Code*・5.6 *Exercises*（問1）（計 164行 / 7,352字）
- **対応する和訳の章・節**: **和訳なし（MIT 最新版での新設章）**（※旧 3.7節 `Code: sbrk` が即時割り当てのみを解説していた箇所の発展形）
- **前提となる回**: 第7回・第8回・第9回・第10回
- **中心概念（2個）**: ① ページフォルト例外（`scause` 13/15 と故障番地 `stval`）を「異常終了」ではなく「その場でページを用意して何事もなかったように再開する合図」に使う発想、② xv6 の遅延メモリ割り当て（`SBRK_LAZY` のサイズ記録だけ行う `sys_sbrk` と、実アクセス時に1ページずつ割り当てる `vmfault`）および `SBRK_EAGER` との使い分け
- **中心の問い**: 「アプリが『念のため 1GB メモリをください』と言ったとき、最初から全部の物理メモリを配らずに『本当に触ったページだけその場で配る』手品はどうやって実現しているの？」
- **主に触れるコード**: `user/ulib.c`（`sbrk`, `sbrklazy`）、`kernel/sysproc.c`（`sys_sbrk`）、`kernel/proc.c`（`growproc`）、`kernel/trap.c`（`usertrap` のページフォルト分岐）、`kernel/vm.c`（`vmfault`, `uvmalloc`, `uvmdealloc`, `uvmunmap`）
- **PC に戻ったときの小さな実験案**: `./scripts/test name sbrklazy` を実行して遅延割り当てテストを通したあと、`kernel/vm.c` の `vmfault` 先頭に1行 `printk`（特定プロセス名のみ）を書くか GDB で `vmfault` にブレークを張り、本当にメモリに触れた瞬間に初めて物理ページが配られる様子を観察する。
- **和訳と今のコードのズレで触れるべき点**: **第5章まるごと和訳には存在しない新設章**であり、これに伴い第5章以降のすべての章番号が和訳からずれる起点になっている点。また `usys.pl` のスタブが `sys_sbrk`（2引数）になり、ユーザー関数 `sbrk`（即時）と `sbrklazy`（遅延）に分かれた点。

---

### 第12回（`ep12`）：現代OSを支えるページフォルト三銃士 ― COW `fork`・デマンドページング・`mmap`
- **対応する MIT の章・節**: Ch.5 5.3 *Real world: Copy-On-Write (COW) fork*・5.4 *Real world: Demand paging*・5.5 *Real world: Memory-mapped files*・5.6 *Exercises*（問2・3）（計 133行 / 6,233字）
- **対応する和訳の章・節**: **和訳なし（MIT 最新版での新設章）**
- **前提となる回**: 第1回・第8回・第11回
- **中心概念（2個）**: ① 親子で物理ページを読み取り専用（`PTE_W` オフ）のまま共有し、書き込んだ瞬間だけページフォルトで複製するコピーオンライト（COW）`fork`、② 実行ファイルやスワップ領域を必要なページだけディスクから読み出し・追い出しするデマンドページングと `mmap`
- **中心の問い**: 「第1回で『`fork` でメモリを丸ごとコピーした直後に `exec` で全部捨てるのはもったいない』という話があったけれど、現代の OS はどうやってコピーせずに `fork` を一瞬で終わらせているの？」
- **主に触れるコード**: `kernel/proc.c`（`kfork`）、`kernel/vm.c`（`uvmcopy`, `vmfault`）、`kernel/exec.c`（`kexec`, `loadseg`）、`kernel/riscv.h`（`PTE_W`, `PTE_V`）
- **PC に戻ったときの小さな実験案**: `kernel/vm.c` の `uvmcopy` を読み、現在の xv6 が `fork` のたびに全ページを `kalloc` ＋ `memmove` で愚直にコピーしている箇所を確認したうえで、「もし COW にするならどの行をどう変え、どこで参照数を数える必要があるか」をメモに書き出してみる。
- **和訳と今のコードのズレで触れるべき点**: 和訳では第3章末尾の *Real world*（3.9節）で数段落だけ触れられていた仮想メモリ応用技術が、MIT 最新版では第5章の独立3節（5.3〜5.5）として具体的な動作手順つきで大幅に拡充された点。

---

### 第13回（`ep13`）：キーボードの1文字が届くまで ― コンソールドライバの表と裏
- **対応する MIT の章・節**: Ch.6 *Interrupts and device drivers* 導入部・6.1 *Code: Console input*・6.2 *Code: Console output*・6.3 *Concurrency in drivers*・6.6 *Exercises*（問1）（計 196行 / 8,771字）
- **対応する和訳の章・節**: 第4章 4.7「デバイスドライバ」・4.8「Code: コンソールドライバ」・4.10「練習問題」（※MIT 6.2 *Console output* と 6.3 *Concurrency in drivers* は独立新設節）
- **前提となる回**: 第2回・第9回・第10回
- **中心概念（2個）**: ① プロセス文脈で動く「上半分（top half：`consoleread` / `consolewrite`）」と割込文脈で動く「下半分（bottom half：`uartintr` / `consoleintr`）」がリングバッファを介して協調する仕組み、② 出力完了割込を使って CPU の空待ちをなくす `uartwrite` と緊急出力用 `uartputc_sync` の使い分け
- **中心の問い**: 「シェルが入力待ちで眠っているあいだに人間がキーを叩くと、CPU はどうやって気づき、バックスペースや改行を整えてシェルに1行分の文字を渡すの？」
- **主に触れるコード**: `kernel/trap.c`（`devintr`）、`kernel/plic.c`（`plicinit`, `plicinithart`, `plic_claim`, `plic_complete`）、`kernel/console.c`（`consoleinit`, `consoleread`, `consolewrite`, `consoleintr`）、`kernel/uart.c`（`uartinit`, `uartwrite`, `uartputc_sync`, `uartintr`）
- **PC に戻ったときの小さな実験案**: `./scripts/run` で xv6 を起動し、シェル上で `Ctrl+P` を押すと `consoleintr` の隠しショートカットで実行中プロセス一覧（`procdump`）が画面に出ることを試してみる！
- **和訳と今のコードのズレで触れるべき点**: ① **章の分離**：和訳の第4章後半が独立して **第6章** になった点、② **送信割込の導入**：和訳の練習問題1だった「UART 出力の割込駆動化」がすでに本番コード（**`uartwrite`**）に実装され、ポーリング出力は `printk`・エコー用の **`uartputc_sync`** に改名された点（練習問題1も逆に「割込を使わない実装へ戻す」に反転）、③ 待機呼び出しが `sleep_prepare` 方式に変わっている点。

---

### 第14回（`ep14`）：OSの心臓を打つメトロノーム ― 新しくなったタイマ割込と高速I/Oの世界
- **対応する MIT の章・節**: Ch.6 6.4 *Timer interrupts*・6.5 *Real world*・6.6 *Exercises*（問2）（計 112行 / 5,628字）
- **対応する和訳の章・節**: 第4章 4.4「タイマ割込」・4.9「世の中のオペレーティングシステム（後半）」
- **前提となる回**: 第4回・第10回・第13回
- **中心概念（2個）**: ① RISC-V の `sstc` 拡張（`time` と `stimecmp` レジスタ）によりスーパーバイザーモードで直接時を刻む `timerinit` / `clockintr` の仕組み、② 割込オーバーヘッドを避けるポーリング・DMA・`ioctl` など現実のデバイス制御の使い分け
- **中心の問い**: 「もし計算に夢中でシステムコールを一切呼ばない無限ループのアプリがいたら、OS はどうやって強制的に CPU を取り戻すきっかけを作るの？」
- **主に触れるコード**: `kernel/start.c`（`timerinit`）、`kernel/trap.c`（`devintr`, `clockintr`）、`kernel/sysproc.c`（`sys_pause`, `sys_uptime`）、`kernel/virtio_disk.c`（`virtio_disk_rw`, `virtio_disk_intr`）
- **PC に戻ったときの小さな実験案**: xv6 シェルで何秒か待ってから新しいプログラムを動かすか、`./scripts/debug` で `ticks` 変数の値を数秒おきに `p ticks` で表示して、約0.1秒ごとに時計が1つずつ進んでいることを確かめる。
- **和訳と今のコードのズレで触れるべき点**: **全面刷新ポイント**：和訳 4.4節で最も難解だった「マシンモードの `CLINT` ＋ スクラッチ配列 ＋ `kernelvec.S` の `timervec` からソフトウェア割込で中継する仕組み」は **完全に廃止・削除** され、現在は `stimecmp` レジスタを使って S-mode の `clockintr()` でシンプルに直接受け取る実装に変わっている点。

---

### 第15回（`ep15`）：2つのCPUが同時に触るとリストが消える？ ― 競合状態とスピンロックの誕生
- **対応する MIT の章・節**: Ch.7 *Locking* 導入部・7.1 *Races*・7.2 *Code: Locks*（計 411行 / 13,722字）
- **対応する和訳の章・節**: 第5章「ロック」導入部・5.1「競合状態」・5.2「Code: ロック」（※章番号 5 → 7）
- **前提となる回**: 第7回（`kfree` のフリーリスト構造）
- **中心概念（2個）**: ① マルチコアで共有データを同時に更新すると片方の変更が消滅する「競合状態（race）」とロックが守る「不変条件（invariant）」、② 普通の `if` 文ではロックを作れない理由と、RISC-V のアトミック交換命令（`amoswap` / `__atomic_exchange_n`）によるスピンロック `acquire` / `release`
- **中心の問い**: 「2つの CPU コアが同時に `kfree` で空きメモリを返却しただけなのに、どうして片方のメモリページが永遠に行方不明になってしまうの？ そして『鍵が空いていたら閉める』という動作自体はどうやって割り込まれずに実行するの？」
- **主に触れるコード**: `kernel/kalloc.c`（`kfree`, `kalloc`）、`kernel/spinlock.h`（`struct spinlock`）、`kernel/spinlock.c`（`initlock`, `acquire`, `release`, `holding`）
- **PC に戻ったときの小さな実験案**: 実験ブランチ（`./scripts/exp nolock-kalloc`）で `kernel/kalloc.c` の `acquire(&kmem.lock)` と `release(&kmem.lock)` を一時的にコメントアウトして `./scripts/run`（3コア起動）で `usertests` や複数コマンドを走らせ、本当にメモリ破壊や `panic` が起きるかを体験して `./scripts/exp back` 前に戻す。
- **和訳と今のコードのズレで触れるべき点**: ① 章番号が **第5章 → 第7章** にずれている点、② `kernel/spinlock.c` で使うコンパイラ組み込み関数が、和訳の旧式 `__sync_lock_test_and_set` / `__sync_lock_release` から、現代的な **`__atomic_exchange_n(..., __ATOMIC_ACQUIRE)` と `__atomic_store_n(..., __ATOMIC_RELEASE)`** に置き換わっている点。

---

### 第16回（`ep16`）：自分自身の首を絞めないために ― デッドロック・ロック順序・割り込み禁止
- **対応する MIT の章・節**: Ch.7 7.3 *Code: Using locks*・7.4 *Deadlock and lock ordering*・7.5 *Locks and interrupts*（計 290行 / 11,158字）
- **対応する和訳の章・節**: 第5章 5.3「Code: ロックを使う」・5.4「デッドロックとロック順序」・5.5「ロックと割込ハンドラ」
- **前提となる回**: 第14回・第15回
- **中心概念（2個）**: ① 複数のロックを取る順序を全体で揃えないと永遠に待ち合う「デッドロック」と、モジュール設計との綱引き、② スピンロック保持中に同じ CPU で割り込みが起きると **1つの CPU 単独でもデッドロックする** 理由と、ネスト回数を数える `push_off` / `pop_off`
- **中心の問い**: 「ロックを丁寧にかければかけるほど安全になるはずなのに、どうして『2つのロックを逆順に取った瞬間』や『ロック中にタイマ割込が来た瞬間』に OS 全体がピタッと凍りついてしまうの？」
- **主に触れるコード**: `kernel/kalloc.c`（`kalloc`, `kfree`）、`kernel/console.c`（`consoleintr`）、`kernel/trap.c`（`clockintr`）、`kernel/spinlock.c`（`acquire`, `release`, `push_off`, `pop_off`）
- **PC に戻ったときの小さな実験案**: `kernel/spinlock.c` の `acquire` 冒頭にある `if(holding(lk)) panic("acquire");` を確認し、なぜ xv6 が同じロックの二度取り（再入）を即座に `panic` で見つける設計にしているかを `push_off` の `noff` カウンタと合わせて読む。
- **和訳と今のコードのズレで触れるべき点**: 7.5節の例で登場する一時停止システムコールの実装関数名が、和訳の `sys_sleep` から **`sys_pause`（`kernel/sysproc.c`）** に改名されている点。

---

### 第17回（`ep17`）：コードの順番どおりに動かない？ ― メモリバリア・アトミック演算・スリープロック
- **対応する MIT の章・節**: Ch.7 7.6 *Instruction and memory ordering*・7.7 *Programming with Atomics*・7.8 *Sleep locks*・7.9 *Real world*・7.10 *Exercises*（計 295行 / 11,561字）
- **対応する和訳の章・節**: 第5章 5.6「命令とメモリの順序」・5.7「スリープロック」・5.8「世の中のオペレーティングシステム」・5.9「練習問題」（※MIT 7.7 *Programming with Atomics* は **和訳なし**）
- **前提となる回**: 第15回・第16回
- **中心概念（2個）**: ① コンパイラと CPU が高速化のために読み書きの順番を入れ替える現象と、それを防ぐ「メモリバリア（fence）」およびロックなしのアトミック命令、② ディスク待ちのような長時間ロックで CPU を譲れる「スリープロック（`sleeplock`）」とスピンロックとの使い分け
- **中心の問い**: 「C言語で『データを書いてからロックを外す』と順番どおり書いたのに、別の CPU から見ると『ロックが外れたのにデータが古いまま』になることがあるのはなぜ？ また、遅いディスク読み書き中にスピンロックを持ってはいけないのはなぜ？」
- **主に触れるコード**: `kernel/spinlock.c`（`acquire`, `release`）、`kernel/sleeplock.h`（`struct sleeplock`）、`kernel/sleeplock.c`（`initsleeplock`, `acquiresleep`, `releasesleep`, `holdingsleep`）
- **PC に戻ったときの小さな実験案**: `xv6-riscv/` をビルドした状態で、`kernel/spinlock.c` の `__ATOMIC_ACQUIRE` / `__ATOMIC_RELEASE` コメントを読み、`acquiresleep` が内部で「短いスピンロック `lk->lk`」を使って「長いスリープロック `lk->locked`」を守っている2重構造を `kernel/sleeplock.c` で確かめる。
- **和訳と今のコードのズレで触れるべき点**: ① **MIT 7.7節 *Programming with Atomics*（`amoadd` 命令や `__atomic_fetch_add`）が新設**された点、② メモリバリアの実装が和訳の `__sync_synchronize()` 単体呼び出しから `__ATOMIC_ACQUIRE` / `__ATOMIC_RELEASE` 指定へ統合された点。

---

### 第18回（`ep18`）：1つのCPUで何十個ものプロセスを回す手品 ― コンテキストスイッチと `swtch`
- **対応する MIT の章・節**: Ch.8 *Scheduling* 導入部・8.1 *Multiplexing*・8.2 *Context switch overview*・8.3 *Code: Context switching*（計 163行 / 6,386字）
- **対応する和訳の章・節**: 第6章「スケジューリング」導入部・6.1「マルチプレクス」・6.2「Code: コンテキストスイッチ」（※章番号 6 → 8、8.2 は独立節化）
- **前提となる回**: 第5回・第9回・第14回
- **中心概念（2個）**: ① プロセスAからプロセスBへ直接飛ばず、必ず「CPU ごとの専用スケジューラスレッド」を中継する2段コンテキストスイッチの全体像、② たった14個のレジスタ（`ra`, `sp`, `s0`〜`s11`）だけを保存・復元して実行の流れをすり替えるアセンブリ関数 `swtch`
- **中心の問い**: 「トラップのときは32個すべてのレジスタを保存したのに、スレッドを切り替える `swtch` ではたった14個しか保存しないのはなぜ？ しかも、どうしてプロセスから次のプロセスへ直接ジャンプしないの？」
- **主に触れるコード**: `kernel/proc.h`（`struct context`, `struct cpu`, `struct proc`）、`kernel/swtch.S`（`swtch`）
- **PC に戻ったときの小さな実験案**: `./scripts/debug` で GDB をつなぎ、`swtch` にブレークポイントを張って `info registers ra sp` を実行し、`swtch` の前後でスタックポインタ `sp` と戻り番地 `ra` が別スレッドのものへ入れ替わる瞬間を目撃する！
- **和訳と今のコードのズレで触れるべき点**: ① 和訳の第6章が MIT 最新版では **第8章（スケジューリング）と第9章（Sleep と Wakeup）に2分割**された点、② `struct cpu` のスケジューラ用コンテキストのメンバ名が、和訳の `c->scheduler` から **`c->context`（`kernel/proc.h`）** に改名された点。

---

### 第19回（`ep19`）：スレッドをまたぐロックのバトンリレー ― `scheduler` と `myproc` の舞台裏
- **対応する MIT の章・節**: Ch.8 8.4 *Code: Scheduling*・8.5 *Code: mycpu and myproc*・8.6 *Real world*・8.7 *Exercises*（計 270行 / 8,244字）
- **対応する和訳の章・節**: 第6章 6.3「Code: スケジューリング」・6.4「Code: `mycpu` と `myproc`」・6.9「世の中のオペレーティングシステム（前半）」・6.10「練習問題（一部）」
- **前提となる回**: 第16回・第18回
- **中心概念（2個）**: ① 「プロセス側で `acquire(&p->lock)` して `swtch` に入り、切り替え先の `scheduler` 側で `release(&p->lock)` する」という世にも珍しいロックのバトンリレーが必要な理由、② `tp` レジスタから現在の CPU 番号を知り、割込禁止でコア移動を防ぎながら `mycpu` / `myproc` を引く仕組み
- **中心の問い**: 「普通はロックを取った関数自身がロックを解放するのに、どうして `yield` では自分が寝たあとに別のスレッドである `scheduler` にロックを外してもらうなんてアクロバットをしているの？」
- **主に触れるコード**: `kernel/proc.c`（`scheduler`, `sched`, `yield`, `forkret`, `cpuid`, `mycpu`, `myproc`）、`kernel/start.c`（`start` の `w_tp`）、`kernel/trampoline.S`（`uservec` の `tp` 設定）
- **PC に戻ったときの小さな実験案**: `kernel/proc.c` の `sched()` にある4つの `panic` チェック（`holding(&p->lock)`、`noff == 1`、`state != RUNNING`、`intr_get() == 0`）を1行ずつ読み、どれか1つでも欠けたらどんな事故が起きるかを確かめる。
- **和訳と今のコードのズレで触れるべき点**: ① `forkret` からの復帰先が和訳の `usertrapret()` 呼び出しから **`prepare_return()` ＋ `trampoline_userret(satp)`** に変わった点、② アイドル時の待機命令 `wfi` まわりや初回プロセスの `kexec("/init", ...)` 呼び出しが `forkret` に統合されている点。

---

### 第20回（`ep20`）：起こす合図を取りこぼすな！ ― 新方式 `sleep_prepare` とパイプの待ち合わせ
- **対応する MIT の章・節**: Ch.9 *Sleep and Wakeup* 導入部・9.1 *Overview*・9.2 *Code: Sleep and wakeup*・9.3 *Code: Pipes*（計 359行 / 12,555字）
- **対応する和訳の章・節**: 第6章 6.5「`sleep` と `wakeup`」・6.6「Code: Sleep と wakeup」・6.7「Code: パイプ」（※独立して第9章へ分離）
- **前提となる回**: 第2回・第16回・第19回
- **中心概念（2個）**: ① 「まだデータがないと確認してから眠りにつく一瞬の隙」に `wakeup` が素通りしてしまう **Lost Wakeup（起床取りこぼし）問題** と、それを解決する最新の `sleep_prepare(chan)` ＋ `sleep()` 方式（およびループ再確認による偽起床対策）、② `pipewrite` と `piperead` が満杯・空のときに眠り、相手を起こし合う実装
- **中心の問い**: 「『パイプが空だったら寝る』と書くとき、ロックを持ったままでは寝られないし、ロックを外してから寝ようとするとその瞬間に相手がデータを書いて起こしに来てすれ違ってしまう！ このジレンマをどうやって解くの？」
- **主に触れるコード**: `kernel/proc.c`（`sleep_prepare`, `sleep`, `wakeup`）、`kernel/pipe.c`（`struct pipe`, `pipealloc`, `pipewrite`, `piperead`, `pipeclose`）
- **PC に戻ったときの小さな実験案**: `kernel/proc.c` の `sleep_prepare`・`sleep`・`wakeup`（合わせて約50行）を開き、「`sleep_prepare` の直後、`sleep` が `p->lock` を取る前に別コアで `wakeup` が走ったら `p->chan` がどうなるか」を1行ずつ指で追って確かめる。
- **和訳と今のコードのズレで触れるべき点**: **超重要差分**：和訳 6.6節では条件ロック `lk` を引数に渡す1関数 **`sleep(chan, lk)`** だったが、現在のコードと MIT 最新版では **`sleep_prepare(chan)` で先に待機チャネルを登録 → 条件ロック `release(lk)` → 引数なしの `sleep()`** を呼ぶ2段階方式（途中で `wakeup` が来たら `p->chan = 0` で眠らず即座に戻る仕組み）に全面変更されている点！

---

### 第21回（`ep21`）：なぜ終了したプロセスは一度「ゾンビ」になるのか ― `exit`・`wait`・`kill` とプロセスロックの総整理
- **対応する MIT の章・節**: Ch.9 9.4 *Code: Wait, exit, and kill*・9.5 *Process Locking*・9.6 *Real world*・9.7 *Exercises*（計 414行 / 14,024字）
- **対応する和訳の章・節**: 第6章 6.8「Code: `wait`, `exit`, および `kill`」・6.9「世の中のオペレーティングシステム（後半）」・6.10「練習問題（一部）」（※MIT 9.5 *Process Locking* は **和訳なし**）
- **前提となる回**: 第1回・第19回・第20回
- **中心概念（2個）**: ① 実行中の自分自身のスタックやページテーブルを自分では解放できないため `ZOMBIE` 状態を経て親の `kwait`（親が先に死ねば `init` への養子縁組 `reparent`）に片付けてもらう仕組みと、フラグを立てて安全地点で自発終了させる `kkill`、② xv6 最難関のロックである `p->lock`（9つの役割）と `wait_lock` の役割分担
- **中心の問い**: 「`exit` したプロセスがその場で自分のメモリを全部片付けて消えればいいのに、どうしてわざわざ『ゾンビ状態』になって親が `wait` するまで居残るの？ そして `kill` されたプロセスがその瞬間に即死しないのはなぜ？」
- **主に触れるコード**: `kernel/proc.c`（`kexit`, `reparent`, `kwait`, `kkill`, `setkilled`, `killed`, `allocproc`, `freeproc`）、`kernel/trap.c`（`usertrap` の `killed(p)` チェック）
- **PC に戻ったときの小さな実験案**: `user/zombie.c` の短いコード（子を作って親が5チック `pause` する間に子が終了する）を読み、xv6 シェルで `zombie &` あるいは `Ctrl+P` をタイミングよく押して `zombie` 状態のプロセス表示を観察する。
- **和訳と今のコードのズレで触れるべき点**: ① 関数名が `wait`/`exit`/`kill` から **`kwait`/`kexit`/`kkill`** に改名された点、② 和訳の `wakeup1` が廃止され、親子関係を守る大域ロック **`wait_lock` が導入**された点、③ **MIT 9.5節 *Process Locking* が新設**され、`p->killed` の直接参照もロック付きの `killed(p)` / `setkilled(p)` に変わった点。

---

### 第22回（`ep22`）：ファイルシステム7階建ての土台 ― ディスク区画とバッファキャッシュ
- **対応する MIT の章・節**: Ch.10 *File system* 導入部・10.1 *Overview*・10.2 *Buffer cache layer*・10.3 *Code: Buffer cache*・10.4 *Code: Block allocator*（計 426行 / 14,191字）
- **対応する和訳の章・節**: 第7章「ファイルシステム」導入部・7.1「概要」・7.2「バッファキャッシュ層」・7.3「Code: バッファキャッシュ」・7.7「Code: ブロックアロケータ」（※章番号 7 → 10、途中の和訳 7.4〜7.6 ロギングは Ch.11 へ移動）
- **前提となる回**: 第3回・第17回（スリープロック）
- **中心概念（2個）**: ① ファイルシステム7層構造の全体見取り図とディスク上の区画配置（ブート・スーパーブロック・ログ・inode・ビットマップ・データブロック）、② 遅いディスクのブロックをメモリ上に1つだけ置いて排他・再利用（LRU）するバッファキャッシュ（`bget` / `bread` / `brelse`）と空きビットを探す `balloc` / `bfree`
- **中心の問い**: 「ただの『1024バイト区画の並び』でしかないディスクの上に、どうやってフォルダやファイルを組み立てるの？ そして2つのプロセスが同じディスク区画を同時に読み書きしようとしたらどうなるの？」
- **主に触れるコード**: `kernel/fs.h`（`struct superblock`）、`kernel/buf.h`（`struct buf`）、`kernel/bio.c`（`binit`, `bget`, `bread`, `bwrite`, `brelse`）、`kernel/fs.c`（`balloc`, `bfree`）
- **PC に戻ったときの小さな実験案**: `kernel/bio.c` の `brelse` で「使い終わったバッファを双方向循環リストの `head.next`（先頭）につなぎ直し、追い出すときは `head.prev`（末尾＝一番古く使われたもの）から探す」約15行の LRU 実装を読んで動きをたどる。
- **和訳と今のコードのズレで触れるべき点**: ① 章番号が **第7章 → 第10章** に移り、和訳では 7.3 の直後にあったロギング層（7.4〜7.6節）が **後ろの第11章へ分離**されて先にファイルシステム全体の縦の繋がりを学べる構成になった点、② `struct buf` の参照数操作に `bpin` / `bunpin` が整理されている点。

---

### 第23回（`ep23`）：ファイルの実体 `inode` を解剖する ― 2つのカウンタと間接ブロックの工夫
- **対応する MIT の章・節**: Ch.10 10.5 *Inode layer*・10.6 *Code: Inodes*・10.7 *Code: Inode content*（計 478行 / 14,786字）
- **対応する和訳の章・節**: 第7章 7.8「inode 層」・7.9「Code: inode」・7.10「Code: inode の中身」
- **前提となる回**: 第3回・第22回
- **中心概念（2個）**: ① ディスク上の `dinode` とメモリ上の `inode`（`itable`）、そして「メモリ上の参照数 `ref`」と「ディスク上の名前数 `nlink`」の2つのカウンタによる寿命管理（＋起動時の孤児回収 `ireclaim`）、② 小さなファイルは高速に直接指し、大きなファイルは間接ブロックで最大 268 ブロックまで伸ばす `bmap` と `readi` / `writei`
- **中心の問い**: 「第3回で『`unlink` で名前を消しても、開いているプロセスがある間はファイルの中身が消えない』と学んだけれど、カーネルの中身ではどうやってそれを管理しているの？ また、もしその途中で電源が切れたらそのファイルはどうなるの？」
- **主に触れるコード**: `kernel/fs.h`（`struct dinode`）、`kernel/file.h`（`struct inode`）、`kernel/fs.c`（`iinit`, `ialloc`, `iget`, `ilock`, `iunlock`, `iput`, `itrunc`, `ireclaim`, `bmap`, `readi`, `writei`）
- **PC に戻ったときの小さな実験案**: `./scripts/test name forphan` を実行し、開いたまま `unlink` されたファイルの途中でクラッシュしても、再起動時の `fsinit` → `ireclaim` が孤児 `inode` を自動で見つけて解放する様子をテストログで確かめる！
- **和訳と今のコードのズレで触れるべき点**: ① メモリ上の `inode` 表の名前が、和訳の `icache` から「データキャッシュではなく参照テーブルである」実態に合わせて **`itable`（`kernel/fs.c`）に改名**された点、② クラッシュ時に `nlink == 0` のまま残った孤児 `inode` を起動時に回収する **`ireclaim` 関数が新設**された点。

---

### 第24回（`ep24`）：スラッシュをたどる旅 ― ディレクトリ・パス名探索・ファイル記述子層
- **対応する MIT の章・節**: Ch.10 10.8 *Code: Directory layer*・10.9 *Code: Path names*・10.10 *File descriptor layer*（計 354行 / 10,167字）
- **対応する和訳の章・節**: 第7章 7.11「Code: ディレクトリ層」・7.12「Code: パス名」・7.13「ファイルディスクリプタ層」
- **前提となる回**: 第2回・第23回
- **中心概念（2個）**: ① ディレクトリの中身は「14文字の名前＋inode番号（`struct dirent`）の配列」にすぎないことと、`/a/b/c` を1階層ずつロックを掛け替えながらたどる `namex`、② パイプ・デバイス・通常ファイルを `struct file` に包み、システム全体のオープンファイル表（`ftable`）とプロセスごとの記述子表（`p->ofile`）の2段で管理する仕組み
- **中心の問い**: 「`/a/b/c` というパス名をたどっている最中に別のプロセスがフォルダを書き換えても壊れず、しかも `.` や `..` があってもデッドロックしないように、`namex` はどうやってロックを掛け替えているの？」
- **主に触れるコード**: `kernel/fs.h`（`struct dirent`）、`kernel/fs.c`（`dirlookup`, `dirlink`, `skipelem`, `namex`, `namei`, `nameiparent`）、`kernel/file.h`（`struct file`, `struct devsw`）、`kernel/file.c`（`filealloc`, `filedup`, `fileclose`, `filestat`, `fileread`, `filewrite`）
- **PC に戻ったときの小さな実験案**: 第2回で学んだ「`fork` や `dup` では読み書き位置（オフセット）が共有され、同じファイルを2回 `open` したときは共有されない理由」を、`p->ofile[fd]` と `ftable.file`（`f->off`）の2段構造に照らして `kernel/file.c` で答え合わせする。
- **和訳と今のコードのズレで触れるべき点**: `struct file` の種別定数や `fileread`/`filewrite` の骨格は共通だが、カレントディレクトリ変数名が MIT 最新版コードでは `cp->cwd` 等に整理され、`stati` 周辺のロック表記が明確化されている点。

---

### 第25回（`ep25`）：すべての層が繋がる瞬間 ― ファイル系システムコールと現実のファイルシステム
- **対応する MIT の章・節**: Ch.10 10.11 *Code: System calls*・10.12 *Real world*・10.13 *Exercises*（計 362行 / 9,932字）
- **対応する和訳の章・節**: 第7章 7.14「Code: システムコール」・7.15「世の中のオペレーティングシステム（ロギング以外）」・7.16「練習問題（ロギング以外）」
- **前提となる回**: 第3回・第22回・第23回・第24回
- **中心概念（2個）**: ① 下位6層を組み合わせて `sys_link`・`sys_unlink`・`create`・`sys_open` が動く全手順（特に複数の `inode` を扱うときのデッドロック回避とトランザクション境界）、② xv6 の単純な配列型ディレクトリや固定ブロック管理と、現代のファイルシステム（B木・ページキャッシュ統合・高度な置換戦略）との対比
- **中心の問い**: 「ファイルに別名を付ける `link` や新しくファイルを作る `open` の裏側では、親ディレクトリと対象ファイルの2つの `inode` をどの順番でロックし、どうやって安全に書き換えているの？」
- **主に触れるコード**: `kernel/sysfile.c`（`sys_link`, `isdirempty`, `sys_unlink`, `create`, `sys_open`, `sys_mkdir`, `sys_mknod`, `sys_chdir`, `sys_pipe`）
- **PC に戻ったときの小さな実験案**: `kernel/sysfile.c` の `sys_unlink` を開き、なぜ `"."` と `".."` だけは絶対に `unlink` できないよう最初に弾いているのか、もしそれを許したら何が起きるかをコードから確かめる。
- **和訳と今のコードのズレで触れるべき点**: `sys_open` に **`O_TRUNC`（既存ファイルを開いたときに `itrunc(ip)` で中身を空にする分岐）** が追加されている点、およびリンク数上限 `NLINK_MAX` のチェック等が整理されている点。

---

### 第26回（`ep26`）：途中で電源が抜けても壊れない秘密 ― 先行書き込みログ（Logging）と復旧
- **対応する MIT の章・節**: Ch.11 *Logging* 導入部・11.1 *Log design*・11.2 *Code: Logging*・11.3 *Real world*・11.4 *Exercises*（計 345行 / 13,227字）
- **対応する和訳の章・節**: 第7章 7.4「ロギング層」・7.5「ログの設計」・7.6「Code: ロギング」・7.15/7.16（ロギング部分）（※独立して第11章へ分離）
- **前提となる回**: 第22回・第23回・第25回
- **中心概念（2個）**: ① 複数のディスク書き換えを「いったんログ領域へ全部書き出し → ヘッダにブロック数を書いた瞬間にコミット成立 → 本来の場所へ反映」する先行書き込みログ（Write-Ahead Logging）と起動時 `recover_from_log`、② 複数のシステムコールを1回のコミットに相乗りさせる「グループコミット（`begin_op` / `end_op`）」と `sync` システムコール
- **中心の問い**: 「ファイルを1つ作るだけでも『inode 割り当て』『ディレクトリ追記』『ビットマップ更新』と何箇所もディスクを書き換えるのに、ちょうどその真ん中でコンセントが抜けてもファイルシステムが矛盾しないのはなぜ？」
- **主に触れるコード**: `kernel/log.c`（`struct logheader`, `struct log`, `initlog`, `begin_op`, `end_op`, `log_write`, `commit`, `write_log`, `write_head`, `install_trans`, `recover_from_log`, `sys_sync`）、`kernel/fs.c`（`fsinit`）、`user/sync.c`（`main`）
- **PC に戻ったときの小さな実験案**: MIT 教科書 11.4 練習問題のとおり、実験ブランチ（`./scripts/exp log-trace`）で `kernel/log.c` の `install_trans` 内に `printk("log write %d\n", log.lh.block[tail]);` を1行だけ追加し、xv6 シェルで `echo hi > f` を実行したときに何個のブロックがどの順でログ経由で書かれるか観察する！
- **和訳と今のコードのズレで触れるべき点**: ① 和訳の第7章途中（7.4〜7.6節）から **独立した第11章** に分離された点、② 保留中のログを確実にディスクへ書き出させる **`sync` システムコール（`sys_sync`）と `user/sync.c` が追加**された点、③ 11.4節の実験コードも `printf` から `printk` になっている点。

---

### 第27回・最終回（`ep27`）：ロックの向こう側と、数千行の旅の終わりに ― 並行性再訪とまとめ
- **対応する MIT の章・節**: Ch.12 *Concurrency revisited* 導入部・12.1 *Locking patterns*・12.2 *Lock-like patterns*・12.3 *No locks at all*・12.4 *Parallelism*・12.5 *Exercises* ＋ Ch.13 *Summary*（`sum.tex`）（計 246行 / 12,452字）
- **対応する和訳の章・節**: 第8章「並行性・再び」導入部・8.1〜8.5 ＋ 第9章「まとめ」（※章番号 8 → 12、9 → 13）
- **前提となる回**: これまでの全回（特に第15回〜第26回）
- **中心概念（2個）**: ① これまでの全サブシステムを貫く並行性デザインパターン（キャッシュの2段ロック、参照数による解放防止、所有権の移転、ロックなし共有を支える暗黙のメモリバリア）、② 「正しさのために並列性を抑えるロック」から「複数コアで同時に速く動かす並列性（Parallelism）」への視点転換と、xv6 で学んだ OS の本質（第13章 *Summary*）
- **中心の問い**: 「単純に『データ1つにロック1つ』では済まない場面を xv6 はどうやって乗り切ってきたのか？ そして数千行の小さなカーネルを最後までたどり終えた今、Linux や現代の巨大な OS を見るときに何が『変わらない本質』として見えてくるのか？」
- **主に触れるコード**: `kernel/bio.c`（`bget`）、`kernel/proc.c`（`yield`, `setkilled`, `killed`, `myproc`, `kfork`, `scheduler`）、`kernel/fs.c`（`ilock`, `namex`）、`kernel/pipe.c`（`pipeclose`, `pipealloc`）、`kernel/kalloc.c`（`kalloc`, `kfree`）、`kernel/main.c`（`main` の `started`）
- **PC に戻ったときの小さな実験案**: `./scripts/test -q`（クイック統合テスト）を自分の手で走らせて `ALL TESTS PASSED` を見届けたあと、`kernel/pipe.c` を開いて「読み手と書き手が別々のロックで同時に動けるパイプ」に改造するならどう設計するか（12.5 練習問題1）を構想してみる。
- **和訳と今のコードのズレで触れるべき点**: ① 章番号が **第8章・第9章 → 第12章・第13章** に移っている点、② 和訳 8.3節では `p->killed` を「ロックなしで共有する変数」の例として挙げていたが、現在のコードと MIT 12.1節では C言語のデータ競合（未定義動作）とコンパイラのレジスタキャッシュを防ぐため **ロック付きの `setkilled` / `killed`（12.1節の例）に改められた**という象徴的な進化点！

# 引き継ぎ・検証記録（NOTES）

更新日: 2026-10-27

## 1. 環境構築フェーズ（完了済み）

### 作成・構成したファイル（初期環境）

- `xv6-riscv/` — `mit-pdos/xv6-riscv`（コミット `e93dabeb98431235c6e1a101cb96c73c923fdbc4`）を `.git` なしで無改変コピー（`xv6-riscv/LICENSE` 保持）
- `.devcontainer/Dockerfile`, `.devcontainer/devcontainer.json` — Ubuntu 26.04 ベースの Codespaces / Dev Container 定義
- `scripts/run`, `scripts/clean`, `scripts/debug`, `scripts/test`, `scripts/qemu_test.py`, `scripts/exp` — ビルド・起動・クリーン・GDB 接続・自動テスト・実験ブランチ切替ラッパー
- `docs/env.md`, `README.md`, `LICENSE`, `VERSIONS.md`, `.gitignore`, `.gitattributes`

### WSL2 Ubuntu 26.04 実機での環境検証要約

- 上流ソース無改変確認、`./scripts/test smoke`、`./scripts/test name copyin`、`./scripts/test -q`（`ALL TESTS PASSED`）、`hello` 一時追加と原状回復、`./scripts/debug` GDB 接続、`./scripts/exp` 動作をすべて確認済み（終了コード 0）。

---

## 2. システムコール教材（現・第4章）・参照自動解決・MkDocs 構築フェーズ

### 今回作成・変更したファイル

- **新規作成**
  - `docs/index.md` — 教材サイトのトップページ（使い方・AI 学習モード案内・章一覧）
  - `docs/ch04-syscall.md`（初出時は旧第1章として作成、のちフェーズ5で MIT 教科書第4章に合わせ改名） — 「第4章 トラップとシステムコール（1）アプリからOSに処理を頼む」（`xv6ref` 自動抜粋、実測ログ、折りたたみ確認問題4問）
  - `docs/labs/syscall-trace.patch` — `echo` プロセスのシステムコール名と戻り値を表示する改造パッチ（`xv6-riscv/kernel/syscall.c` 対象）
  - `docs/requirements.txt` — MkDocs 依存定義（`mkdocs==1.6.1`, `mkdocs-material==9.8.0`）
  - `docs/xv6refs.lock` — 全コード参照の行範囲と SHA-256 ロックファイル
  - `mkdocs.yml` — MkDocs（Material テーマ・日本語設定・`mkdocs_xv6refs.py` フック）
  - `scripts/xv6refs.py` — C 関数・アセンブリラベル・Perl サブルーチンの抽出、GitHub 固定コミットリンク生成、ロック照合ロジック
  - `scripts/mkdocs_xv6refs.py` — ビルド時に `<!-- xv6ref: path#symbol -->` を展開する MkDocs hook
  - `scripts/check-refs` — 全参照の解決と `docs/xv6refs.lock` 整合性検証（`--update` 対応）
  - `scripts/check-lab` — `docs/labs/<名前>.patch` の一時適用・ビルド・QEMU 自動検証・原状回復スクリプト
  - `GEMINI.md`, `AGENTS.md` — 学習モード選択・`scripts/exp` 利用・読む範囲制限・`docs/` 参照を定めた同内容のエージェント指示書
  - `.github/workflows/pages.yml` — `check-refs` と `mkdocs build --strict` を実行して GitHub Pages へデプロイする Actions ワークフロー（未 push）
- **更新**
  - `docs/env.md` — MkDocs 厳格ビルド対応およびサイトビルド・`check-refs`・`check-lab` 手順を追記
  - `.devcontainer/Dockerfile`, `.devcontainer/devcontainer.json` — `python3-venv` / `python3-pip` と `/opt/mkdocs`（`docs/requirements.txt`）を追加、`postCreateCommand` に `check-refs` / `check-lab` を追加（Docker ビルド未検証を明記）
  - `.gitignore` — `/site/` と `/.venv/` を追加
  - `VERSIONS.md`, `README.md`, `NOTES.md` — 追加ツール・構成・検証記録を反映

### 検証コマンドと結果

- `./scripts/check-lab syscall-trace`（`logs/lab-syscall-trace.log`）: **PASS**（パッチ一時適用 → ビルド → QEMU 起動 → `echo hi` の3行出力と `ls` 非出力を確認 → パッチ逆適用・SHA-256 一致確認・`make clean`）
- `./scripts/check-refs --update` / `./scripts/check-refs`: **PASS**（6参照すべて解決・ロック一致）
- 意図的な参照破壊テスト（`logs/check-refs-broken.log`）: **期待どおり失敗（exit 1）を確認後に復元**
  - 存在しない関数名（`kernel/syscall.c#nosuchfunc`）: 該当行番号と対象参照を表示して失敗
  - コード内容変更（パッチ一時適用による `kernel/syscall.c#syscall` 変化）: `docs/ch04-syscall.md`（当時旧名）の `kernel/syscall.c#syscall` ハッシュ不一致を表示して失敗
- `mkdocs build --strict`（`logs/mkdocs-build.log`）: **PASS**（警告・エラー 0、生成 HTML 内の6つの固定コミット GitHub リンク・Mermaid・補足ボックス・`<details>` 展開を確認）
- `./scripts/test smoke && ./scripts/clean`: **PASS**（無改変 `xv6-riscv/` のビルド・起動・テスト通過と生成物削除を確認）
- `cmp -s GEMINI.md AGENTS.md`: **PASS**（完全一致）

### 第4章（`docs/ch04-syscall.md`）本文の主張とソース照合チェックリスト

- [x] 対象コミットが `e93dabeb98431235c6e1a101cb96c73c923fdbc4` — `VERSIONS.md`
- [x] U-mode では `PTE_U` のないページへアクセス不可、ユーザーページテーブルにはカーネル本体やデバイスが無く `TRAMPOLINE` / `TRAPFRAME` にも `PTE_U` が付かない — `kernel/riscv.h` (`PTE_U`), `kernel/proc.c` (`proc_pagetable`), `kernel/vm.c` (`kvmmake`)
- [x] 引数は `a0`〜`a5`（xv6 は最大6個、`a6` は未使用）、番号は `a7`、戻り値は `a0` — `user/usys.pl` (`entry`), `kernel/syscall.c` (`argraw`, `syscall`), `kernel/trampoline.S` (`userret`)
- [x] `SYS_write` の番号は `16` — `kernel/syscall.h`
- [x] `ecall` で S-mode 昇格・割り込み停止、`sepc` に `ecall` 番地保存、`scause` に `8` 記録、`stvec`（`uservec`）へ遷移し、`satp`・`sp`・汎用レジスタは自動切替されない — `kernel/trap.c` (`usertrap`, `prepare_return`), `kernel/trampoline.S` (`uservec`)
- [x] `TRAMPOLINE` はユーザー・カーネル両ページテーブルの同一最高番地（`MAXVA - PGSIZE`）に配置、`TRAPFRAME` はその1ページ下 — `kernel/memlayout.h`, `kernel/proc.c` (`proc_pagetable`), `kernel/vm.c` (`kvmmake`)
- [x] `uservec` が `sscratch` に `a0` を退避後 `TRAPFRAME` へ全ユーザーレジスタを保存（元の `a0` は `112(a0)`）し、`kernel_sp`・`kernel_hartid`・`kernel_trap`・`kernel_satp` を読んで `satp` 切替後に `usertrap` へ飛ぶ — `kernel/trampoline.S` (`uservec`), `kernel/proc.h` (`struct trapframe`)
- [x] `usertrap` が `stvec` を `kernelvec` に切替、`sepc` を `p->trapframe->epc` に保存、`r_scause() == 8` で `epc += 4`（`ecall` は4バイト命令）・`intr_on()` 後に `syscall()` を呼び、`prepare_return()` を経てユーザー `satp` を返す — `kernel/trap.c` (`usertrap`, `prepare_return`)
- [x] `userret` がユーザー `satp` へ戻し、`TRAPFRAME` からレジスタ復元（`a0` に戻り値）後 `sret` で U-mode の次命令へ復帰 — `kernel/trampoline.S` (`userret`)
- [x] `usys.pl` から `perl user/usys.pl > user/usys.S` でスタブ生成、`sbrk` のみ `sys_sbrk` ラベル（`user/ulib.c` の `sbrk` / `sbrklazy` から呼出） — `Makefile`, `user/usys.pl`, `user/ulib.c`
- [x] `syscall()` が `p->trapframe->a7` から `syscalls[num]()` を呼び戻り値を `p->trapframe->a0` に格納、未定義番号は `printk` して `-1` — `kernel/syscall.c` (`syscall`)
- [x] `sys_kill(void)` が `argint(0, &pid)` で `p->trapframe->a0` を取り出し `kkill(pid)`（成功 `0` / 失敗 `-1`）を返す — `kernel/sysproc.c` (`sys_kill`), `kernel/syscall.c` (`argint`, `argraw`), `kernel/proc.c` (`kkill`)
- [x] `echo hi` のトレース結果（`3: syscall exec -> 2`、`hi3: syscall write -> 2`、改行後の `3: syscall write -> 1`、`exit` 非表示、`ls` 非表示）とその理由 — `kernel/exec.c` (`kexec`), `user/echo.c` (`main`), `kernel/sysfile.c` (`sys_write`), `kernel/proc.c` (`kexit`), `logs/lab-syscall-trace.log`
- [x] 省略事項（`fetchstr` / `copyin` / `copyinstr`、M-mode の `start.c` における `medeleg` / `mideleg` 委譲） — `kernel/syscall.c`, `kernel/vm.c`, `kernel/start.c`

---

## 3. 未確認事項（Mac / Windows / Codespaces / GitHub 側で要確認）

- **Docker ビルド・コンテナ起動（MkDocs 導入を含む）**: この WSL 環境では Docker デーモンを使用できないため、更新後の `.devcontainer/Dockerfile`（`python3-venv` / `python3-pip` および `/opt/mkdocs` への MkDocs 導入を含む）のイメージビルドと `devcontainer.json` による起動は未検証。
- **GitHub Actions による GitHub Pages デプロイ**: `git commit` / `git push` を行っていないため、`.github/workflows/pages.yml` の GitHub 上での実稼働と Pages 公開設定（Settings → Pages → Source: GitHub Actions）は push 後に要確認。
- **コミット後の `./scripts/exp syscall-trace` 実操作**: 本作業では指示に従い `git commit` を行っていないため（未コミットファイルがある状態では `scripts/exp` が安全停止する設計）、コミット後に `exp/syscall-trace` ブランチ切替を確認可能（過去フェーズで一時クローン上の `scripts/exp` 動作自体は確認済み）。
- **Mac / Windows / Codespaces 実機動作・Gemini CLI 初回認証・`./scripts/test full`**: 引き続き実機側で要確認。

---

## 4. 第1回音声解説台本・読み方辞書作成フェーズ

- **作成ファイル**: `video/ep01/reference-analysis.md`、`video/ep01/script.md`、`video/ep01/dictionary.csv`、`video/ep01/description.txt`、`scripts/script-stats`
- **集計・検証結果（`./scripts/script-stats --check`）**: **PASS**（6セクション・85文、本文 3,594字［句読点除き 3,367字］、推定尺 10分53秒〜11分59秒［330〜300字/分換算］、英字トークン20種すべて `dictionary.csv` 登録済み、画面依存表現ゼロ、話者名「ナビ」は先頭メタ情報1か所のみ）
- **「耳だけで聞く人」視点の通読セルフチェックで修正した点**:
  1. **前提説明の補完**: 初出の「ページ」「シェル」「プロセス」「子プロセス」にその場で短い言い換え（「メモリ1区画、つまり1ページ分」「コマンドを受け付けるシェル」「実行中のプログラム、つまりプロセス」「分身のプロセス」）を追加し、理由番号 `8` にも「割り込みなど他の用事と見分ける理由番号」と目的を添えた。
  2. **同音異義・英字過多の解消**: `echo` 実験の `hi`（ハイ）が日本語の返事「はい」に聞こえないよう「英語の挨拶である2文字の hi」と補足し、レジスタ名の読み上げを `a0` と `a7` の2つに絞って（`a1`・`a2`・`a5` や `sscratch` 退避の細部アセンブリ説明を削減）耳での記憶負荷と説明の飛躍をなくした。
  3. **前後の繋がりと間の調整**: 第4節の戻り値「2」が唐突に聞こえないよう第4節冒頭で「write を呼んで2文字出すとき」と明示し、`exec` の未説明な戻り値読み上げを整理し、2つ目の問いかけの直後にも考える間（「ちょっと考えてみてね。」）を1文追加した。

---

## 5. 教科書（MIT 最新版・菅原訳）連携・章番号統一・差分整理フェーズ

### 作成・変更したファイル

- **新規作成**
  - `books/README.md` — `books/mit-en/`（MIT 原文 `fa3b46bc`、2026-09-23）と `books/sugawara-ja/`（菅原訳 `de6c710a`、2020-07-23、元原文 `ca13de46`、2019-10-08）の出典・ライセンス・参照専用（ビルド不要）である旨の記録
  - `docs/books-map.md` — MIT 最新版（全13章＋序文）・菅原訳（全9章＋序文）・本教材ページの全章・全節対応表と、2019 年版から最新版への章新設・分割・移動の整理
  - `docs/books/trap-diff.md` — 菅原訳 第4章（`trap.tex`）と現在の `xv6-riscv/`（および MIT 最新版）のコード・記述差分一覧、ならびに `\lineref` 照合表
- **改名・更新**
  - `docs/ch04-syscall.md`（旧ファイルから改名） — タイトルを「第4章 トラップとシステムコール（1）アプリからOSに処理を頼む」に変更し、冒頭に対応教科書（MIT 4.1〜4.4節／菅原訳 4.1・4.3・4.5・4.6節）、末尾に第9節「教科書と並べて読むときの注意」を追加
  - `docs/xv6refs.lock` — `./scripts/check-refs --update` により参照元パスを `docs/ch04-syscall.md` へ更新
  - `mkdocs.yml`, `docs/index.md`, `docs/env.md`, `README.md`, `VERSIONS.md` — 教科書情報、新章番号（第4章）、`books-map.md` / `books/trap-diff.md` への導線を反映
  - `AGENTS.md`, `GEMINI.md`（同内容） — 教科書に関する質問時に `books/` の必要な章・節のみを読むこと、和訳と現在のコードのズレは最新原文・現コードを優先して明示すること（`docs/books-map.md` / `docs/books/*-diff.md` 参照）を追加
  - `video/ep01/script.md`, `video/ep01/description.txt`, `video/ep01/dictionary.csv` — 参照章パスおよび章番号表記を `docs/ch04-syscall.md`（第4章）へ更新

### 検証コマンドと結果

- 旧第1章ファイル名プレフィックスの残存検索（`.git` / `site` / `logs` 除外の `grep -rn`）: **0件**（取りこぼしなし）
- `./scripts/check-refs`: **PASS**（6参照すべてロック一致）
- `mkdocs build --strict`: **PASS**（警告・エラー 0）
- `./scripts/check-lab syscall-trace`: **PASS**（パッチ一時適用 → QEMU 検証 → 逆適用・クリーンアップ成功）
- `./scripts/script-stats --check`: **PASS**（85文・3,594字・辞書未登録ゼロ）
- `cmp -s GEMINI.md AGENTS.md`: **PASS**（完全一致）
- `diff -r -x .git` による `books/mit-en/`・`books/sugawara-ja/` と取り込み元との一致確認、および `xv6-riscv/` 無変更確認: **PASS**

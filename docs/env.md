# xv6 実験環境ガイド

このリポジトリのルートで以下のコマンドを実行します。`xv6-riscv/` は [MIT PDOS の通常版 xv6-riscv](https://github.com/mit-pdos/xv6-riscv) を `.git` なしで無改変のまま取り込んだものです。また `books/` には MIT の xv6 教科書（英語原文）と電気通信大学・菅原研究室による和訳の LaTeX ソースを参照用として無改変で収録しています（ビルドは不要です。章・節の対応は [教科書との対応表](books-map.md) を参照してください）。採用コミットと実測したツールの版はリポジトリ直下の `VERSIONS.md`、検証記録は `NOTES.md` を参照してください。

通常の `xv6-riscv` は xv6 カーネル本体と標準ユーザープログラム（`sh`、`ls`、`usertests` など）のみで構成されたシンプルなリポジトリです。一方、MIT の講義 6.1810 で使われるラボ用リポジトリ（`xv6-labs-20xx`）は年度・課題ごとに調整されており、課題ごとのブランチ、学習者が実装するための未完成コード、採点スクリプト（`make grade`）や課題専用テストを含みます。通常版では `make grade` などは使えないため、この環境では通常版に含まれる `usertests` や `forktest` を `scripts/test` から実行します（講義の課題に取り組む場合は、その年度の `xv6-labs-20xx` を別途用意してください）。

## Mac / Windows で開く

未コミットの編集内容まで同じ環境で共有したい場合は、Mac と Windows の両方から**同じ既存の GitHub Codespace** を開きます。ローカル Dev Container は各端末に独立した作業コピーを持つため、端末間の同期には Git の commit / push / pull を使います。

| 端末 | Codespaces で開く（ローカル Docker 不要） | ローカル Dev Container で開く |
| --- | --- | --- |
| Mac | ブラウザーで GitHub リポジトリ → `Code` → `Codespaces` → `Create codespace on master`。2 回目以降は Codespaces 一覧から同じ環境を開く。 | Docker Desktop を起動し、VS Code に Dev Containers 拡張を入れる。リポジトリのルートを開き、`Cmd+Shift+P` → `Dev Containers: Reopen in Container`。 |
| Windows | ブラウザーで同じ GitHub アカウントにログインし、上と同じ操作（作成済みなら一覧から同じ Codespace を開く）。 | WSL2（Ubuntu）、Docker Desktop（WSL 2 エンジンと対象 Ubuntu の WSL Integration を有効化）、Windows 版 VS Code、WSL 拡張・Dev Containers 拡張を入れる。WSL 側のホーム配下に clone して `code .` で開き、`Ctrl+Shift+P` → `Dev Containers: Reopen in Container`。 |

コンテナ起動後、VS Code のターミナルで `./scripts/test smoke` を実行して動作確認します。`.devcontainer/` の設定を変更した場合は `Dev Containers: Rebuild Container`（Codespaces では `Codespaces: Rebuild Container`）を実行してください。

`.devcontainer/Dockerfile` は `ubuntu:26.04` ベースで、QEMU、RISC-V 向け GCC / binutils、`gdb-multiarch`、`make`、`python3`（`venv` / `pip` 含む）、`expect`、Node.js / npm、Gemini CLI（`@google/gemini-cli`）、および教材サイト用の MkDocs（`/opt/mkdocs` 仮想環境）を導入します。apt パッケージ名と Python パッケージ構成は WSL2 Ubuntu 26.04 実機で確認したものと揃えていますが、開発環境で Docker が使えないため **Dockerfile 自体のビルドおよび Mac / Windows / Codespaces 実機での起動は未検証**です。Gemini CLI の認証は、コンテナ起動後に `gemini` を実行して各自で行ってください。

## 起動・終了・再ビルド

```sh
./scripts/run                 # make qemu：必要な部分をビルドして起動
```

`init: starting sh` に続いて `$` が出たら xv6 のシェルです。

```text
ls
echo hello xv6
cat README
```

終了は **`Ctrl-a` を押して離し、続けて `x`** です（ホストのターミナルへ戻ります）。ソースを編集したら再度 `./scripts/run` で差分ビルド・起動できます。クリーンビルドする場合は `./scripts/clean` の後に `./scripts/run` を実行します。`./scripts/run CPUS=1` のように `make` 変数を渡すこともできます。

`xv6-riscv/fs.img` が仮想ディスクです。`./scripts/clean` やユーザープログラム更新時には `fs.img` が再生成され、xv6 内で作ったファイルは消えます。残したいコードは必ずホスト側で編集・保存してください。また、同じ作業ツリーで複数の QEMU（`run` / `debug` / `test`）を同時起動しないでください。

## テスト

```sh
./scripts/test smoke          # 起動、ls / echo / cat README、forktest（約 10 秒）
./scripts/test                # 既定：usertests -q（短縮版）
./scripts/test quick          # 同上：slowtests を省く短縮版
./scripts/test -q             # quick の別名
./scripts/test name copyin    # usertests の指定テスト 1 件のみ実行
./scripts/test full           # usertests 全体（長時間）
```

Python 標準ライブラリのみで QEMU の標準入出力を制御し、`ALL TESTS PASSED`（または期待出力）とシェルプロンプトへの復帰を確認して `Ctrl-a x` で自動終了します（無限実行型の `grind` は対象外）。実行ログは `logs/test-<モード>.log` に保存されます（`XV6_TEST_LOG` で変更可、Git 管理外）。既定タイムアウトは `smoke` 120 秒、`quick` / `name` 600 秒、`full` 1,800 秒で、遅い環境では `XV6_TEST_TIMEOUT=1200 ./scripts/test -q` のように延長できます。

## デバッグ

同じコンテナ（または WSL）内の同じ作業コピーでターミナルを 2 つ開きます。

```sh
# ターミナル 1：make qemu-gdb（CPU を停止して GDB 接続を待つ）
./scripts/debug
```

```sh
# ターミナル 2：生成された .gdbinit を読み込んで gdb-multiarch で接続
./scripts/debug connect
```

GDB 接続後の操作例：

```text
(gdb) break main
(gdb) continue
(gdb) next
(gdb) info registers
(gdb) detach
(gdb) quit
```

実行中に止める場合は GDB 側で `Ctrl-c`、終了時は `detach` → `quit`、QEMU 本体の終了はターミナル 1 で `Ctrl-a` → `x` です。接続ポートは UID から自動計算されます（確認は `make -C xv6-riscv print-gdbport`、変更は `./scripts/debug GDBPORT=26001`）。

## 実験ブランチ

コード改造を試すときは、作業ツリーがクリーンな状態で `exp/<名前>` ブランチを切って作業します（未コミットの変更がある状態や初回コミット前の状態では、誤操作防止のためスクリプトが停止します）。

```sh
./scripts/exp hello           # 現在のブランチを記録し、exp/hello を作成・切替
# コード変更・実行・テスト
./scripts/exp back            # 記録した元のブランチへ戻る（変更を commit または取り消してから実行）
```

### 小さな変更の例（`hello` コマンドの追加）

1. `./scripts/exp hello` で実験ブランチへ切り替えます。
2. `xv6-riscv/user/hello.c` を作成します：
   ```c
   #include "kernel/types.h"
   #include "user/user.h"

   int
   main(void)
   {
     printf("hello xv6\n");
     exit(0);
   }
   ```
3. `xv6-riscv/Makefile` の `UPROGS` 末尾に `\t$U/_hello\` を追加し、`./scripts/run` で起動して xv6 シェルから `hello` を実行します。
4. 実験を残す場合は `exp/hello` に `git commit` してから `./scripts/exp back` で `master` に戻ります。破棄する場合は変更を元に戻し、`./scripts/clean` してから `./scripts/exp back` を実行します（`master` には変更を残しません）。

## WSL2 Ubuntu で Docker を使わず直接動かす場合

Ubuntu 26.04（WSL2）では、以下のパッケージを導入すればコンテナなしで同じスクリプトを実行できます（この Ubuntu 版では RISC-V 用 QEMU 本体が `qemu-system-riscv` に分離されているため両方指定します）。

```sh
sudo apt-get update
sudo apt-get install --no-install-recommends \
  qemu-system-misc qemu-system-riscv gcc-riscv64-linux-gnu binutils-riscv64-linux-gnu \
  gdb-multiarch build-essential make python3 python3-venv python3-pip expect bc perl git ca-certificates sudo
./scripts/test smoke
./scripts/test -q
```

## 教材サイトのビルドと参照・実験チェック

教材ページ（`docs/`）は MkDocs（Material テーマ）で静的サイトとしてビルド・プレビューできます。本文中のコード抜粋（`<!-- xv6ref: ファイル#関数 -->`）はビルド時に `xv6-riscv/` から自動生成されます。

```sh
# ローカル環境で MkDocs を仮想環境に入れる場合（コンテナ内では /opt/mkdocs に導入済み）
python3 -m venv .venv
.venv/bin/pip install -r docs/requirements.txt

# コード参照とロックファイル（docs/xv6refs.lock）の整合チェック
./scripts/check-refs

# 厳格モードで静的サイトを site/ にビルド
mkdocs build --strict

# 手元でプレビューサーバーを起動（http://127.0.0.1:8000）
mkdocs serve

# 教材の改造実験パッチを一時適用して自動検証（完了後に自動で元へ戻す）
./scripts/check-lab syscall-trace
```

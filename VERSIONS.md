# バージョン情報

確認日: 2026-10-27

## 取り込んだ xv6

- 上流リポジトリ: <https://github.com/mit-pdos/xv6-riscv>
- ブランチ: `riscv`
- コミット ID: `e93dabeb98431235c6e1a101cb96c73c923fdbc4`
- コミット日時・件名: `2026-10-26 17:16:16 -0400` (`tx_busy`)
- 配置先: `xv6-riscv/`（`.git` ディレクトリを除き、ソース無改変でコピー）

## 取り込んだ教科書（参照用 LaTeX ソース）

ビルドは行わず、章・節の特定やコードとの差分照合に用いるため `.git` ディレクトリを除き無改変で配置しています（詳細は [`books/README.md`](books/README.md) を参照）。

### 1. MIT xv6 教科書（英語原文）

- 上流リポジトリ: <https://github.com/mit-pdos/xv6-riscv-book>
- コミット: `fa3b46bc4386fcd2c2a042f3dc850c497948b6d6`（`2026-09-23`）
- 取り込み日: `2026-10-27`
- ライセンス: MIT License（`books/mit-en/LICENSE`）
- 配置先: `books/mit-en/`（`.git` 除外・無改変）

### 2. 電気通信大学・菅原研究室による和訳

- 上流リポジトリ: <https://github.com/sugawara-bbbb/xv6-riscv-book>
- コミット: `de6c710ac79883a2bc68a9b9f70c1fc22de48d39`（`2020-07-23`）
- 元になった英語原文: `mit-pdos/xv6-riscv-book` コミット `ca13de462d1936f4ff3c249fcbc261fc93c48b53`（`2019-10-08`）
- 取り込み日: `2026-10-27`
- ライセンス: MIT License（`books/sugawara-ja/LICENSE`）
- 配置先: `books/sugawara-ja/`（`.git` 除外・無改変）

## 検証ホスト環境

- OS: Ubuntu 26.04.1 LTS (Resolute Raccoon)
- カーネル: `Linux 6.18.54.1-microsoft-standard-WSL2 x86_64`

## 実測したツールの版（WSL2 Ubuntu 26.04）

| ツール / コマンド | 実測バージョン | 導入パッケージ / 備考 |
| --- | --- | --- |
| `qemu-system-riscv64` | QEMU emulator version `10.2.1` | `qemu-system-riscv` (`1:10.2.1+ds-1ubuntu3.3`), `qemu-system-misc` (`1:10.2.1+ds-1ubuntu3.3`) |
| `riscv64-linux-gnu-gcc` | `15.2.0` (Ubuntu 15.2.0-16ubuntu1) | `gcc-riscv64-linux-gnu` (`4:15.2.0-5ubuntu1`) |
| `riscv64-linux-gnu-objdump` / `ld` | GNU Binutils `2.46` | `binutils-riscv64-linux-gnu` (`2.46-3ubuntu2`) |
| `gdb-multiarch` | GNU gdb `17.1` (Ubuntu 17.1-2ubuntu1) | `gdb-multiarch` (`17.1-2ubuntu1`) |
| `gcc`（ホスト `mkfs` 用） | `15.2.0` (Ubuntu 15.2.0-16ubuntu1) | `build-essential` (`12.12ubuntu2.26.04.2`) |
| `make` | GNU Make `4.4.1` | `make` (`4.4.1-3`) |
| `python3` | Python `3.14.4` | `python3` (`3.14.3-0ubuntu2`), `python3-venv` (`3.14.3-0ubuntu2`), `python3-pip` (`25.1.1+dfsg-1ubuntu2`) |
| `mkdocs` | `1.6.1` | `/opt/mkdocs` 仮想環境に `docs/requirements.txt`（`mkdocs==1.6.1`, `mkdocs-material==9.8.0`）を導入 |
| `expect` | `5.45.4` | `expect` (`5.45.4-4build1`) |
| `bc` | `1.07.1` | `bc` (`1.07.1-4build1`) |
| `perl` | `v5.40.1` | `perl` (`5.40.1-7ubuntu0.3`) |
| `git` | `2.53.0` | `git` (`1:2.53.0-1ubuntu1.1`) |
| `node` | `v24.21.0` | WSL 既存の NodeSource 版 `nodejs` (`24.21.0-1nodesource1`) |
| `npm` | `11.19.0` | 上記 `nodejs` に同梱 |
| `gemini` | `0.65.0` | `@google/gemini-cli@0.65.0`（`npm install -g`） |

## Dev Container との差分・補足（未検証）

- `.devcontainer/Dockerfile` は `ubuntu:26.04` をベースとし、xv6 のビルド・実行・デバッグに必要な apt パッケージ名と `/opt/mkdocs` への MkDocs（`docs/requirements.txt`）導入を上記 WSL 実機と揃えています（Docker がこの環境で使えないため、コンテナのビルド自体は未検証）。
- Ubuntu 26.04 では `qemu-system-riscv64` 本体が `qemu-system-misc` から分離された `qemu-system-riscv` に入っているため、両方を指定しています。
- Node.js / npm について、この WSL 実機では導入済みの NodeSource 版 `nodejs` (`24.21.0`, `npm` 同梱) を使用しました。一方 `.devcontainer/Dockerfile` では外部 PPA を増やさず Ubuntu 26.04 標準リポジトリ（`universe`）の `nodejs`（候補版 `22.22.1+dfsg+~cs22.19.15-1ubuntu1`、`@google/gemini-cli@0.65.0` の要件 `node >= 20` を満たす）と `npm`（候補版 `9.2.0~ds3-1`）を指定しています。

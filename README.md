# xv6-riscv 学習・実験環境

MIT PDOS の教育用 OS である RISC-V 版 [xv6 (`xv6-riscv`)](https://github.com/mit-pdos/xv6-riscv) を読み解き、実際に改造・検証しながら OS の仕組みを学ぶための実験環境です。Mac と Windows の両方から GitHub Codespaces または VS Code Dev Containers（および WSL2 Ubuntu 直実行）で同じコードを開き、短いラッパースクリプトですぐにビルド・QEMU 起動・GDB デバッグ・自動テストを行えます。

## リポジトリ構成

- `xv6-riscv/` — 上流 `mit-pdos/xv6-riscv` のソース一式（`.git` 除外・無改変、採用コミットは [VERSIONS.md](VERSIONS.md) 参照）
- `docs/` — 日本語教材と環境ガイド（[トップ](docs/index.md)、[環境ガイド](docs/env.md)、[第1章 システムコール](docs/ch01-syscall.md)、改造パッチ `docs/labs/`、参照ロック `docs/xv6refs.lock`）
- `mkdocs.yml`, `.github/workflows/pages.yml` — MkDocs（Material）設定と GitHub Pages ビルド定義
- `.devcontainer/` — GitHub Codespaces / VS Code Dev Containers 設定（Ubuntu 26.04 ベース、QEMU・RISC-V ツールチェーン・GDB・MkDocs・Gemini CLI 入り、Docker ビルドは未検証）
- `scripts/` — 操作・検証用ラッパー（`run`, `clean`, `debug`, `test`, `exp`, `check-refs`, `check-lab`）
- `GEMINI.md`, `AGENTS.md` — 学習サポート用 AI エージェント指示書
- `VERSIONS.md` — 取り込んだ xv6 のコミット ID と検証済みツールのバージョン
- `NOTES.md` — 環境構築・教材検証結果の記録と未確認事項

## 最初の一歩

1. **環境を開く**: GitHub Codespaces、VS Code Dev Containers、または WSL2 Ubuntu でこのリポジトリを開きます（Mac / Windows 別の手順は [docs/env.md](docs/env.md) を参照）。
2. **動作確認（スモークテスト）**:
   ```sh
   ./scripts/test smoke
   ```
3. **xv6 を対話起動する**:
   ```sh
   ./scripts/run
   ```
   `$` プロンプトが出たら `ls` や `cat README` を試せます。終了は **`Ctrl-a` を押して離し、続けて `x`** です。
4. **教材を読む・検証する・改造実験を試す**:
   - 第1章を読む: [docs/ch01-syscall.md](docs/ch01-syscall.md)（ローカル閲覧は `mkdocs serve`、ビルド確認は `mkdocs build --strict`）
   - コード参照チェック: `./scripts/check-refs`
   - 第1章の改造実験の自動検証: `./scripts/check-lab syscall-trace`
   - 短縮テスト: `./scripts/test -q`（`usertests -q`）
   - GDB デバッグ: `./scripts/debug` と別端末で `./scripts/debug connect`
   - 実験ブランチ作成: `./scripts/exp <名前>`（元に戻るには `./scripts/exp back`）
   - 詳しい手順は [docs/env.md](docs/env.md) を参照してください。

## ライセンス

- このリポジトリの環境構築ファイル・スクリプト・ドキュメントは [MIT License](LICENSE) の下で公開しています。
- `xv6-riscv/` ディレクトリ内の xv6 本体は MIT PDOS による [MIT License](xv6-riscv/LICENSE) です。

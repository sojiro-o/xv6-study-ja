# xv6-riscv 学習・実験環境

MIT PDOS の教育用 OS である RISC-V 版 [xv6 (`xv6-riscv`)](https://github.com/mit-pdos/xv6-riscv) を読み解き、実際に改造・検証しながら OS の仕組みを学ぶための実験環境です。Mac と Windows の両方から GitHub Codespaces または VS Code Dev Containers（および WSL2 Ubuntu 直実行）で同じコードを開き、短いラッパースクリプトですぐにビルド・QEMU 起動・GDB デバッグ・自動テストを行えます。

## リポジトリ構成

- `xv6-riscv/` — 上流 `mit-pdos/xv6-riscv` のソース一式（`.git` 除外・無改変、採用コミットは [VERSIONS.md](VERSIONS.md) 参照）
- `books/` — MIT の xv6 教科書（英語原文 `mit-en/`）と電気通信大学・菅原研究室による和訳（`sugawara-ja/`）の参照用 LaTeX ソース（`.git` 除外・無改変、ビルド不要、出典は [books/README.md](books/README.md) と [VERSIONS.md](VERSIONS.md) 参照）
- `docs/` — 日本語教材と環境ガイド（[トップ](docs/index.md)、[環境ガイド](docs/env.md)、[教科書との対応表](docs/books-map.md)、[第4章 トラップとシステムコール（1）](docs/ch04-syscall.md)、[第4章 差分メモ](docs/books/trap-diff.md)、改造パッチ `docs/labs/`、参照ロック `docs/xv6refs.lock`）
- `mkdocs.yml`, `.github/workflows/pages.yml` — MkDocs（Material）設定と GitHub Pages ビルド定義
- `.devcontainer/` — GitHub Codespaces / VS Code Dev Containers 設定（Ubuntu 26.04 ベース、QEMU・RISC-V ツールチェーン・GDB・MkDocs・Gemini CLI 入り、Docker ビルドは未検証）
- `scripts/` — 操作・検証用ラッパー（`run`, `clean`, `debug`, `test`, `exp`, `check-refs`, `check-lab`）
- `AGENTS.md`, `GEMINI.md`, `CLAUDE.md` — 学習サポート用 AI エージェント指示書
- `VERSIONS.md` — 取り込んだ xv6・教科書のコミット ID と検証済みツールのバージョン
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
   - 第4章（トラップとシステムコール）を読む: [docs/ch04-syscall.md](docs/ch04-syscall.md)（MIT 教科書との対応表は [docs/books-map.md](docs/books-map.md)、ローカル閲覧は `mkdocs serve`、ビルド確認は `mkdocs build --strict`）
   - コード参照チェック: `./scripts/check-refs`
   - 第4章の改造実験の自動検証: `./scripts/check-lab syscall-trace`
   - 短縮テスト: `./scripts/test -q`（`usertests -q`）
   - GDB デバッグ: `./scripts/debug` と別端末で `./scripts/debug connect`
   - 実験ブランチ作成: `./scripts/exp <名前>`（元に戻るには `./scripts/exp back`）
   - 詳しい手順は [docs/env.md](docs/env.md) を参照してください。

## エージェントと一緒に学ぶ

リポジトリのルートでエージェントを起動すると、`AGENTS.md`（Gemini CLI は `GEMINI.md`、Claude Code は `CLAUDE.md` 経由）を読み、最初に学習モードを聞いてきます。

- **解説のみ**: コードや概念を説明するだけ。ファイルは書き換えない。
- **ヒント**: 手がかりだけ出す。ファイルは書き換えない。
- **実装込み**: `./scripts/exp <名前>` で切った実験ブランチで書き換え、ビルド・実行して、理由・差分・結果を説明する。

頼み方の例:

- 「解説のみで。`kernel/syscall.c` の `syscall` が何をしているか、第4章に沿って教えて」
- 「解説のみで。和訳教科書の4.3節にある `usertrapret` が今のコードに見当たらないんだけど、どう変わったの？」
- 「ヒントで。`exit` もトレースに出すにはどうすればいい？」
- 「実装込みで。`getppid` システムコールを追加して、動くところまで見せて」

教材は `mkdocs serve` を実行してブラウザで <http://localhost:8000> を開くと、手元で読めます（公開版: <https://sojiro-o.github.io/xv6-study-ja/>）。

## ライセンス

- このリポジトリの環境構築ファイル・スクリプト・ドキュメントは [MIT License](LICENSE) の下で公開しています。
- `xv6-riscv/` ディレクトリ内の xv6 本体は MIT PDOS による [MIT License](xv6-riscv/LICENSE) です。
- `books/` ディレクトリ内の xv6 教科書（英語原文および菅原研究室による和訳）は MIT License（[books/mit-en/LICENSE](books/mit-en/LICENSE)、[books/sugawara-ja/LICENSE](books/sugawara-ja/LICENSE)）です。

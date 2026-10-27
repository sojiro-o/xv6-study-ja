# 参照用 xv6 教科書ソース（`books/`）

このディレクトリには、学習者が普段読んでいる **MIT の xv6 教科書（英語原文）** と **電気通信大学・菅原研究室による日本語訳** の LaTeX ソースを、それぞれ `.git` ディレクトリを除いて**無改変のまま**収録しています。

## 目的と扱い（ビルド不要）

- これらのファイルは PDF や HTML をビルドするためのものではありません（TeX 環境の導入や `make` の実行は不要です）。
- 教材ページ（`docs/`）の執筆・保守や、AI エージェントが学習者の質問（「教科書の第◯章◯節にこう書いてあるが、今のコードのどこに対応するのか？」など）に正確に答えるための**参照・照合用データ**として配置しています。
- 各サブディレクトリ（`books/mit-en/`、`books/sugawara-ja/`）内のファイルは上流の無改変コピーとして保持し、編集しません。

章・節の対応関係と、2019 年版ベースの和訳と現在の `xv6-riscv/` コードとの差分については、以下を参照してください。

- 教科書全体の章・節対応表: [`../docs/books-map.md`](../docs/books-map.md)
- 第4章（トラップとシステムコール）の和訳・コード差分メモ: [`../docs/books/trap-diff.md`](../docs/books/trap-diff.md)

## 収録している教科書一覧

### 1. `books/mit-en/` — MIT xv6 教科書（英語原文）

- **出典リポジトリ**: <https://github.com/mit-pdos/xv6-riscv-book>
- **コミット ID**: `fa3b46bc4386fcd2c2a042f3dc850c497948b6d6`（コミット日: `2026-09-23`）
- **取り込み日**: `2026-10-27`
- **ライセンス**: MIT License（[`books/mit-en/LICENSE`](mit-en/LICENSE) を保持）

### 2. `books/sugawara-ja/` — 電気通信大学・菅原研究室による日本語訳

- **出典リポジトリ**: <https://github.com/sugawara-bbbb/xv6-riscv-book>
- **コミット ID**: `de6c710ac79883a2bc68a9b9f70c1fc22de48d39`（コミット日: `2020-07-23`）
- **和訳の元になった原文コミット**: `mit-pdos/xv6-riscv-book` の `ca13de462d1936f4ff3c249fcbc261fc93c48b53`（`2019-10-08`）
- **取り込み日**: `2026-10-27`
- **ライセンス**: 原文と同じ MIT License（[`books/sugawara-ja/LICENSE`](sugawara-ja/LICENSE) および [`books/sugawara-ja/README.md`](sugawara-ja/README.md) を保持）

> **注意**: 和訳（`books/sugawara-ja/`）は 2019 年 10 月時点の英語原文をもとに翻訳されているため、本リポジトリの `xv6-riscv/`（2026 年 10 月時点、[`../VERSIONS.md`](../VERSIONS.md) 参照）および最新の英語原文（`books/mit-en/`）とは章番号・関数名・内部実装にズレがあります。

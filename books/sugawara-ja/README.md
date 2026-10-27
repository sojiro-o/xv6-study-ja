# この文書について

以下の Web ページで，コンパイル済みの PDF を配布しています: [電気通信大学・菅原研究室](https://www.sugawara-lab.jp/lecture.html)．

この文書は，
https://github.com/mit-pdos/xv6-riscv-book
で公開されている RISC-V 版 xv6 のテキストを和訳したものです．

対応する RISC-V 版 xv6 のソースコードは以下です．
https://github.com/mit-pdos/xv6-riscv

# ビルド方法

プリプロセッサである lineref が，ファイル中の lineref コマンド（例: `\lineref{kernel/proc.h:/^struct.context/}`）を見つけ，ソースコードを参照して行番号を入力する．生成したコードは latex.out/ に入る．

lineref のために，ソースコードの場所を指定する必要がある．デフォルトでは，カレントディレクトリに xv6-riscv-src という名前でソースコードのディレクトリが必要．以下のようにしてビルドできる．

``` shell
% cd xv6-riscv-book
% git clone https://github.com/mit-pdos/xv6-riscv.git xv6-riscv-src
% make
```

# ビルドに関する変更点

日本語を扱うために，pdflatex から platex に変更した．それに伴い，Makefile と book.tex の微調整を行った．

# ライセンス

元の文書は MIT ライセンスで公開されています（LICENSE を参照）．ここで公開する訳文も同ライセンスに従います．


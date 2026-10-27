# 未検証: この作業環境では Docker を使えないため、イメージの build/run（MkDocs 導入ステップを含む）は未実施。
# xv6 用および Python venv/pip の apt パッケージ名と docs/requirements.txt は WSL2 Ubuntu 26.04 で確認。
# Ubuntu 26.04 の RISC-V 本体は qemu-system-misc から分離された qemu-system-riscv。
# Node.js / npm は Ubuntu 標準リポジトリのパッケージ名を指定（WSL 実機は既存の NodeSource 版 nodejs を使用）。
FROM ubuntu:26.04

ARG GEMINI_CLI_VERSION=0.65.0
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PATH="/opt/mkdocs/bin:${PATH}"

COPY docs/requirements.txt /tmp/docs-requirements.txt

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        qemu-system-misc \
        qemu-system-riscv \
        gcc-riscv64-linux-gnu \
        binutils-riscv64-linux-gnu \
        gdb-multiarch \
        make \
        python3 \
        python3-venv \
        python3-pip \
        expect \
        build-essential \
        bc \
        perl \
        git \
        ca-certificates \
        sudo \
        nodejs \
        npm \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m venv /opt/mkdocs \
    && /opt/mkdocs/bin/pip install --no-cache-dir -r /tmp/docs-requirements.txt \
    && rm -f /tmp/docs-requirements.txt \
    && npm install --global --no-audit --no-fund "@google/gemini-cli@${GEMINI_CLI_VERSION}" \
    && npm cache clean --force

# Ubuntu イメージに既存の UID 1000 がある場合は、そのユーザーを再利用する。
RUN if id ubuntu >/dev/null 2>&1; then \
        usermod --login vscode ubuntu \
        && groupmod --new-name vscode ubuntu \
        && usermod --home /home/vscode --move-home --shell /bin/bash vscode; \
    else \
        groupadd --gid 1000 vscode \
        && useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash vscode; \
    fi \
    && printf 'vscode ALL=(ALL) NOPASSWD:ALL\n' > /etc/sudoers.d/vscode \
    && chmod 0440 /etc/sudoers.d/vscode

USER vscode
WORKDIR /home/vscode
CMD ["sleep", "infinity"]

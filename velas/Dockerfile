FROM --platform=linux/amd64 debian:bullseye-slim

ARG RELEASE="v0.6.3"

ENV DEBIAN_FRONTEND=noninteractive \
    USERNAME=appuser \
    APP_PATH=/data

RUN apt update && \
    apt -y dist-upgrade && \
    apt install -y --no-install-recommends \
        tzdata \
        ca-certificates \
        wget \
        lbzip2 && \
    rm -rf /var/cache/apt/* && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/velas/velas-chain/releases/download/${RELEASE}/velas-release-x86_64-unknown-linux-gnu.tar.bz2 \
    && tar -xvf velas-release-x86_64-unknown-linux-gnu.tar.bz2 \
    && cd velas-release \
    && chmod -R +x bin/ \
    && mv bin/* /usr/local/bin/

RUN groupadd -g 1001 ${USERNAME} \
    && useradd -m -d ${APP_PATH} -u 1001 -g 1001 ${USERNAME}

WORKDIR ${APP_PATH}
USER ${USERNAME}

ENTRYPOINT ["velas-validator"]

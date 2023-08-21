FROM debian:bullseye

ARG RELEASE="v1.1.0"

ENV USERNAME=appuser \
    APP_PATH=/data
ENV DEBIAN_FRONTEND=noninteractive

RUN groupadd -g 1001 ${USERNAME} \
    && useradd -m -d ${APP_PATH} -u 1001 -g 1001 ${USERNAME}

RUN apt update && \
    apt -y dist-upgrade && \
    apt install -y --no-install-recommends \
        unzip \
        wget \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/oasysgames/oasys-validator/releases/download/${RELEASE}/geth-${RELEASE}-linux-amd64.zip \
    && unzip geth-${RELEASE}-linux-amd64.zip \
    && rm geth-${RELEASE}-linux-amd64.zip \
    && mv geth /usr/local/bin/ \
    && chmod +x /usr/local/bin/geth

RUN wget https://github.com/oasysgames/oasys-validator/releases/download/${RELEASE}/genesis.zip \
    && unzip genesis.zip  \
    && rm genesis.zip \
    && mv genesis/mainnet.json /genesis.json \
    && rm -r genesis

EXPOSE 30301 30301/udp 8545

USER ${USERNAME}
WORKDIR /data
ENTRYPOINT ["geth"]

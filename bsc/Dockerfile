FROM debian:bullseye

ARG RELEASE="v1.1.18_hf"

WORKDIR /root

RUN apt-get update && apt-get install -y wget \
    && rm -rf /var/lib/apt/lists/*

# grabs the latest release of BSC from Github
RUN wget https://github.com/bnb-chain/bsc/releases/download/${RELEASE}/geth_linux \
    && mv geth_linux /usr/local/bin/geth \
    && chmod +x /usr/local/bin/geth

COPY ./genesis.json /root/genesis.json
COPY ./config.toml /root/config.toml

EXPOSE 30303 30303/udp 8545

CMD geth --config /root/config.toml --datadir /root/.ethereum --diffsync --cache 8000 --rpc.allow-unprotected-txs --txlookuplimit 0

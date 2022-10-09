FROM debian:bullseye-slim

ARG BSC_RELEASE="v1.1.15"

WORKDIR /root

RUN apt-get update && apt-get install -y \
      wget \
      curl \
      jq \
    && rm -rf /var/lib/apt/lists/*

# grabs the latest release of BSC from Github
RUN wget https://github.com/bnb-chain/bsc/releases/download/${BSC_RELEASE}/geth_linux \
    && mv geth_linux /usr/local/bin/geth \
    && chmod +x /usr/local/bin/geth

COPY ./genesis.json /root/genesis.json
COPY ./config.toml /root/config.toml

EXPOSE 30303 30303/udp 8545

CMD geth --config /root/config.toml --datadir /root/.ethereum --diffsync --cache 8000 --rpc.allow-unprotected-txs --txlookuplimit 0

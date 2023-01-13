FROM golang:1.19.4-bullseye AS build-env

ARG EVMOS_REPO="https://github.com/evmos/evmos.git"
ARG RELEASE="v10.0.1"
ARG EMVOS_GENESIS_JSON="https://archive.evmos.org/mainnet/genesis.json"

WORKDIR /go/src/github.com/evmos/evmos

RUN apt update && \
    apt install git unzip -y

RUN git clone --depth 1 -b ${RELEASE} ${EVMOS_REPO} .

RUN wget ${EMVOS_GENESIS_JSON}
RUN make build

#==============================================================
FROM debian:bullseye-slim as execution

RUN apt update && \
    apt -y dist-upgrade && \
    apt install -y --no-install-recommends \
        tzdata \
        ca-certificates \
        jq && \
    rm -rf /var/cache/apt/*

WORKDIR /root

COPY --from=build-env /go/src/github.com/evmos/evmos/build/evmosd /usr/bin/evmosd
COPY --from=build-env /go/src/github.com/evmos/evmos/genesis.json /root/genesis.json

# Copy configs
COPY ./app.toml /root/.evmosd/config/app.toml
COPY ./client.toml /root/.evmosd/config/client.toml
COPY ./config.toml /root/.evmosd/config/config.toml

COPY ./entrypoint.sh /root/entrypoint.sh
RUN chmod +x /root/entrypoint.sh

EXPOSE 26656 26657 1317 9090 8545 8546

CMD ["evmosd"]

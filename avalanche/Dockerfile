ARG AVALANCHE_REPO="https://github.com/ava-labs/avalanchego.git"
ARG AVALANCHE_RELEASE="v1.10.3"

ARG AVALANCHE_SUBNETS_REPO="https://github.com/ava-labs/subnet-evm"
ARG AVALANCHE_SUBNETS_RELEASE="v0.5.1"

ARG AVALANCHE_CHAIN_ASSETS_REPO="https://github.com/ava-labs/public-chain-assets"

ARG DFK_ETH_CHAIN_ID="53935"
ARG DFK_VM_ID="mDV3QWRXfwgKUWb9sggkv4vQxAQR4y2CyKrt5pLZ5SzQ7EHBv"
ARG DFK_BLOCKCHAIN_ID="q2aTwKuyzgs8pynF7UXBZCU7DejbZbZ6EUyHr3JQzYgwNPUPi"

ARG SWIMMER_ETH_CHAIN_ID="73772"
ARG SWIMMER_VM_ID="srSGD5JeYhL8GLx4RUw53VN5TcoBbax6EeCYmy5S3DiteJhdF"
ARG SWIMMER_BLOCKCHAIN_ID="2K33xS9AyP9oCDiHYKVrHe7F54h2La5D8erpTChaAhdzeSu2RX"

FROM golang:1.19-bullseye AS builder

ARG AVALANCHE_REPO
ARG AVALANCHE_RELEASE

ARG AVALANCHE_SUBNETS_REPO
ARG AVALANCHE_SUBNETS_RELEASE

ARG AVALANCHE_CHAIN_ASSETS_REPO

ARG DFK_VM_ID
ARG SWIMMER_VM_ID

RUN apt-get update && \
    apt-get install -y --no-install-recommends git bash make gcc musl-dev ca-certificates linux-headers-amd64

# Build Avalanche
WORKDIR /avalanchego

RUN git clone --depth 1 -b ${AVALANCHE_RELEASE} ${AVALANCHE_REPO} .

RUN scripts/build.sh

# Build subnets
WORKDIR /subnet-evm

RUN git clone --depth 1 -b ${AVALANCHE_SUBNETS_RELEASE} ${AVALANCHE_SUBNETS_REPO} .

RUN ./scripts/build.sh /avalanchego/build/plugins/${DFK_VM_ID}
RUN ./scripts/build.sh /avalanchego/build/plugins/${SWIMMER_VM_ID}

# Get chain assets
WORKDIR /public-chain-assets

RUN git clone --depth 1 ${AVALANCHE_CHAIN_ASSETS_REPO} .

FROM debian:bullseye-slim as execution

ARG DFK_ETH_CHAIN_ID
ARG DFK_BLOCKCHAIN_ID

ARG SWIMMER_ETH_CHAIN_ID
ARG SWIMMER_BLOCKCHAIN_ID

ENV DEBIAN_FRONTEND=noninteractive \
    USERNAME=appuser \
    APP_PATH=/data

RUN apt update && \
    apt -y dist-upgrade && \
    apt install -y --no-install-recommends \
        tzdata \
        ca-certificates && \
    rm -rf /var/cache/apt/*

RUN groupadd -g 1001 ${USERNAME} \
    && useradd -m -d ${APP_PATH} -u 1001 -g 1001 ${USERNAME}

COPY --from=builder /avalanchego/build/* /usr/local/bin/

# Copy upgrade.json
COPY --from=builder /public-chain-assets/chains/${DFK_ETH_CHAIN_ID}/upgrade.json /home/${DFK_BLOCKCHAIN_ID}/upgrade.json
COPY --from=builder /public-chain-assets/chains/${SWIMMER_ETH_CHAIN_ID}/upgrade.json /home/${SWIMMER_BLOCKCHAIN_ID}/upgrade.json

COPY ./config.json /home/config.json
COPY ./dfk_config.json /home/${DFK_BLOCKCHAIN_ID}/config.json
COPY ./cb_config.json /home/${SWIMMER_BLOCKCHAIN_ID}/config.json

VOLUME ${APP_PATH}

WORKDIR ${APP_PATH}
USER ${USERNAME}

ENTRYPOINT ["avalanchego"]

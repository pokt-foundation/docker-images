ARG AVALANCHE_REPO="https://github.com/ava-labs/avalanchego.git"
ARG AVALANCHE_RELEASE="v1.9.0"

ARG AVALANCHE_SUBNETS_REPO="https://github.com/ava-labs/subnet-evm"
ARG AVALANCHE_SUBNETS_RELEASE="v0.4.0"

ARG DFK_ETH_CHAIN_ID="53935"
ARG DFK_VM_ID="mDV3QWRXfwgKUWb9sggkv4vQxAQR4y2CyKrt5pLZ5SzQ7EHBv"
ARG DFK_BLOCKCHAIN_ID="q2aTwKuyzgs8pynF7UXBZCU7DejbZbZ6EUyHr3JQzYgwNPUPi"

ARG SWIMMER_ETH_CHAIN_ID="73772"
ARG SWIMMER_VM_ID="srSGD5JeYhL8GLx4RUw53VN5TcoBbax6EeCYmy5S3DiteJhdF"
ARG SWIMMER_BLOCKCHAIN_ID="2K33xS9AyP9oCDiHYKVrHe7F54h2La5D8erpTChaAhdzeSu2RX"

FROM golang:1.18.5-buster AS builder

ARG AVALANCHE_REPO
ARG AVALANCHE_RELEASE

ARG AVALANCHE_SUBNETS_REPO
ARG AVALANCHE_SUBNETS_RELEASE

ARG DFK_VM_ID
ARG SWIMMER_VM_ID

RUN apt-get update && \
    apt-get install -y --no-install-recommends git bash=5.0-4 git=1:2.20.1-2+deb10u3 make=4.2.1-1.2 gcc=4:8.3.0-1 musl-dev=1.1.21-2 ca-certificates=20200601~deb10u2 linux-headers-amd64

# Build Avalanche
WORKDIR /avalanchego

RUN git clone --depth 1 -b ${AVALANCHE_RELEASE} ${AVALANCHE_REPO} .

RUN go mod download

RUN ./scripts/build.sh

# Build subnets
WORKDIR /subnet-evm

RUN git clone --depth 1 -b ${AVALANCHE_SUBNETS_RELEASE} ${AVALANCHE_SUBNETS_REPO} .

RUN ./scripts/build.sh /avalanchego/build/plugins/${DFK_VM_ID}
RUN ./scripts/build.sh /avalanchego/build/plugins/${SWIMMER_VM_ID}

FROM debian:buster-slim as execution

ARG DFK_ETH_CHAIN_ID
ARG DFK_BLOCKCHAIN_ID

ARG SWIMMER_ETH_CHAIN_ID
ARG SWIMMER_BLOCKCHAIN_ID

WORKDIR /avalanchego/build

COPY --from=builder /avalanchego/build/ .

# Copy upgrade.json
COPY --from=builder /subnet-evm/networks/mainnet/${DFK_ETH_CHAIN_ID}/upgrade.json /home/${DFK_BLOCKCHAIN_ID}/upgrade.json
COPY --from=builder /subnet-evm/networks/mainnet/${SWIMMER_ETH_CHAIN_ID}/upgrade.json /home/${SWIMMER_BLOCKCHAIN_ID}/upgrade.json

COPY ./config.json /home/config.json

COPY ./dfk_config.json /home/${DFK_BLOCKCHAIN_ID}/config.json
COPY ./cb_config.json /home/${SWIMMER_BLOCKCHAIN_ID}/config.json

ENTRYPOINT ["./avalanchego"]

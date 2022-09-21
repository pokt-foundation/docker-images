FROM golang:1.18.5-buster AS build-env

ARG EVMOS_REPO="https://github.com/evmos/evmos.git"
ARG EVMOS_RELEASE="v8.0.0"
ARG EMVOS_GENESIS_JSON="https://archive.evmos.org/mainnet/genesis.json"

WORKDIR /go/src/github.com/evmos/evmos

RUN apt update
RUN apt install git unzip -y

RUN git clone --depth 1 -b ${EVMOS_RELEASE} ${EVMOS_REPO} .

RUN wget ${EMVOS_GENESIS_JSON}

RUN make build

FROM debian:buster-slim as execution

RUN apt update
RUN apt install ca-certificates jq -y

WORKDIR /root

COPY --from=build-env /go/src/github.com/evmos/evmos/build/evmosd /usr/bin/evmosd
COPY --from=build-env /go/src/github.com/evmos/evmos/genesis.json /root/genesis.json

# Copy configs
COPY ./app.toml /root/.evmosd/config/app.toml
COPY ./client.toml /root/.evmosd/config/client.toml
COPY ./config.toml /root/.evmosd/config/config.toml

COPY ./entrypoint.sh /root/entrypoint.sh
RUN chmod +x /root/entrypoint.sh

EXPOSE 26656 26657 1317 9090

CMD ["evmosd"]

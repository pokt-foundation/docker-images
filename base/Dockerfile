# syntax=docker/dockerfile:1-labs
############ Build OP_NODE
FROM golang:1.19 as op-node

WORKDIR /app

ENV REPO=https://github.com/ethereum-optimism/optimism
ENV RELEASE_OP_NODE="v1.1.1"

ADD $REPO/archive/refs/tags/op-node/$RELEASE_OP_NODE.tar.gz ./
RUN tar -xvf ./$RELEASE_OP_NODE.tar.gz --strip-components=1 && \
    cd op-node && \
    make op-node

########### Build OP_GETH
FROM golang:1.19 as op-geth

ENV REPO=https://github.com/ethereum-optimism/op-geth
ENV RELEASE_OP_GETH="v1.101106.0"

WORKDIR /app
ADD $REPO/archive/refs/tags/$RELEASE_OP_GETH.tar.gz ./
RUN tar -xvf ./$RELEASE_OP_GETH.tar.gz --strip-components=1 && \
    go run build/ci.go install -static ./cmd/geth

############ Base configs
FROM debian:12 as base-config

ARG REPO="https://github.com/base-org/node"
ARG RELEASE_BASE="v0.3.0"

WORKDIR /app
ADD $REPO/archive/refs/tags/$RELEASE_BASE.tar.gz ./
RUN tar -xvf ./$RELEASE_BASE.tar.gz --strip-components=1

##################################
FROM debian:12

RUN apt-get update && \
    apt-get install -y jq curl && \
    rm -rf /var/lib/apt/lists

ENV USERNAME=appuser \
    APP_PATH=/data

COPY --from=op-node /app/op-node/bin/op-node /usr/local/bin/
COPY --from=op-geth /app/build/bin/geth /usr/local/bin/
# COPY --from=builder /app/node/geth-entrypoint .
# COPY --from=builder /app/node/op-node-entrypoint .
COPY --from=base-config /app/goerli /app/goerli
COPY --from=base-config /app/mainnet /app/mainnet

RUN  chmod a+x /usr/local/bin/geth /usr/local/bin/op-node

RUN groupadd -g 1001 ${USERNAME} \
    && useradd -m -d ${APP_PATH} -u 1001 -g 1001 ${USERNAME}

WORKDIR ${APP_PATH}
USER ${USERNAME}

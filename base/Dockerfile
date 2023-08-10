# syntax=docker/dockerfile:1-labs
FROM golang:1.19 as op

ARG GIT_URL="https://github.com/base-org/node.git"
ARG RELEASE="v0.3.0"

RUN apt-get update && \
    apt-get install -y jq curl git && \
    rm -rf /var/lib/apt/lists

RUN git clone $GIT_URL 

WORKDIR /app

ENV REPO=https://github.com/ethereum-optimism/optimism
ENV VERSION=v1.1.1
ENV CHECKSUM=c0f3dbce8729016103b8390f9ee81089cd858242df6a45a42c59555f1c9e9106
ADD --checksum=sha256:$CHECKSUM $REPO/archive/op-node/$VERSION.tar.gz ./

RUN tar -xvf ./$VERSION.tar.gz --strip-components=1 && \
    cd op-node && \
    make op-node

FROM golang:1.19 as geth

WORKDIR /app

ENV REPO=https://github.com/ethereum-optimism/op-geth
ENV VERSION=v1.101106.0
ENV CHECKSUM=0273ea3226147ba5b04c1a6eff2d9da48e6bbff3a348b33fe13e7e34d88ba411
ADD --checksum=sha256:$CHECKSUM $REPO/archive/$VERSION.tar.gz ./

RUN tar -xvf ./$VERSION.tar.gz --strip-components=1 && \
    go run build/ci.go install -static ./cmd/geth

FROM golang:1.19 as builder

ARG GIT_URL="https://github.com/base-org/node.git"
ARG RELEASE="v0.3.0"

WORKDIR /app

RUN apt-get update && \
    apt-get install -y jq curl git && \
    rm -rf /var/lib/apt/lists

RUN git clone $GIT_URL 

FROM golang:1.19

RUN apt-get update && \
    apt-get install -y jq curl && \
    rm -rf /var/lib/apt/lists

ENV USERNAME=appuser \
    APP_PATH=/data

WORKDIR /app


COPY --from=op /app/op-node/bin/op-node /usr/local/bin/
COPY --from=geth /app/build/bin/geth /usr/local/bin/
COPY --from=builder /app/node/geth-entrypoint .
COPY --from=builder /app/node/op-node-entrypoint .
COPY --from=builder /app/node/goerli ./goerli
COPY --from=builder /app/node/mainnet ./mainnet

RUN  chmod a+x /usr/local/bin/geth /usr/local/bin/op-node

RUN groupadd -g 1001 ${USERNAME} \
    && useradd -m -d ${APP_PATH} -u 1001 -g 1001 ${USERNAME}

WORKDIR ${APP_PATH}
USER ${USERNAME}
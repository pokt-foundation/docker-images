FROM --platform=linux/amd64 rust:1.70.0 AS builder

ARG GIT_URL="https://github.com/MystenLabs/sui"
ARG RELEASE="mainnet-v1.6.3"

#build-base linux-headers git bash ca-certificates libstdc++
RUN apt update && \
    apt install -y --no-install-recommends \
        tzdata \
        ca-certificates \
        cmake \
        clang \
        git \
        bash

RUN git clone --depth 1 --branch $RELEASE $GIT_URL /src
WORKDIR /src
RUN cargo build --profile release --bin sui-node

#==============================================================
FROM debian:bullseye-slim as execution

ENV DEBIAN_FRONTEND=noninteractive \
    USERNAME=appuser \
    APP_PATH=/data

RUN apt update && \
    apt -y dist-upgrade && \
    apt install -y --no-install-recommends \
        tzdata \
        ca-certificates \
        libjemalloc-dev && \
    rm -rf /var/cache/apt/*

ENV LD_PRELOAD /usr/lib/x86_64-linux-gnu/libjemalloc.so

COPY --from=builder /src/target/release/sui-node /usr/local/bin

RUN groupadd -g 1001 ${USERNAME} \
    && useradd -m -d ${APP_PATH} -u 1001 -g 1001 ${USERNAME}

WORKDIR ${APP_PATH}
USER ${USERNAME}
VOLUME ${APP_PATH}

ENTRYPOINT ["/usr/local/bin/sui-node"]

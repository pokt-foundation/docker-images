FROM --platform=linux/amd64 golang:bullseye AS builder

ARG KAVA_GIT_URL="https://github.com/kava-labs/kava.git"

ARG KAVA_RELEASE="v0.23.0"

ARG ROCKSDB_GIT_URL="https://github.com/facebook/rocksdb.git"

ARG ROCKSDB_RELEASE="v7.9.2"

RUN apt update && \
    apt -y dist-upgrade && \
    apt install -y --no-install-recommends \
        tzdata \
        liblz4-dev \
        libzstd-dev \
        libjemalloc-dev \
        libsnappy-dev \
        zlib1g-dev \
        curl \
        git \
        make \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN git clone $ROCKSDB_GIT_URL

RUN cd rocksdb && \
    git checkout $ROCKSDB_RELEASE && \
    make -j $(nproc --all) install-shared && \
    ldconfig

RUN git clone $KAVA_GIT_URL && \
    cd kava && \
    git checkout v0.23.0 && \
    make install COSMOS_BUILD_OPTIONS=rocksdb


ENV DEBIAN_FRONTEND=noninteractive
ENV USERNAME=appuser \
    APP_PATH=/data

RUN groupadd -g 1001 ${USERNAME} \
    && useradd -m -d ${APP_PATH} -u 1001 -g 1001 ${USERNAME} \
    && chmod 0755 /go/bin/kava \
    && ldconfig

EXPOSE 8545 30303 30303/udp
VOLUME ${APP_PATH}

WORKDIR ${APP_PATH}
USER ${USERNAME}

ENTRYPOINT ["kava"]
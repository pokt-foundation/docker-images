FROM ubuntu:22.04

ARG KAVA_GIT_URL="https://github.com/kava-labs/kava.git"
ARG KAVA_RELEASE="v0.23.0"
ARG ROCKSDB_GIT_URL="https://github.com/facebook/rocksdb.git"
ARG ROCKSDB_RELEASE="v7.9.2"

RUN apt update && \
    apt -y dist-upgrade && \
    DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends \
        build-essential \
        jq \
        golang-go \
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
    git checkout $KAVA_RELEASE && \
    make install COSMOS_BUILD_OPTIONS=rocksdb

RUN mv /root/go/bin/kava /bin/kava && ldconfig

ENTRYPOINT ["kava"]
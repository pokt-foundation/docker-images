FROM --platform=linux/amd64 ubuntu:22.04

ARG KAVA_GIT_URL="https://github.com/kava-labs/kava.git"
ARG KAVA_RELEASE="v0.23.0"
ARG ROCKSDB_GIT_URL="https://github.com/facebook/rocksdb.git"
ARG ROCKSDB_RELEASE="v7.9.2"

RUN apt update && \
    apt -y dist-upgrade && \
    DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends \
        build-essential \
        jq \
        tzdata \
        liblz4-dev \
        libgflags-dev \
        libzstd-dev \
        libjemalloc-dev \
        libsnappy-dev \
        zlib1g-dev \
        libbz2-dev \
        curl \
        wget \
        git \
        make \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN git clone $ROCKSDB_GIT_URL

RUN cd rocksdb && \
    git checkout $ROCKSDB_RELEASE && \
    make -j $(nproc --all) install-shared && \
    ldconfig

RUN wget https://go.dev/dl/go1.20.4.linux-amd64.tar.gz \
    && tar -C /usr/local -xzf go1.20.4.linux-amd64.tar.gz \
    && rm go1.20.4.linux-amd64.tar.gz

ENV GOPATH=/go \
    PATH=$GOPATH/bin:/usr/local/go/bin:$PATH

RUN mkdir -p "$GOPATH/src" "$GOPATH/bin" && chmod -R 777 "$GOPATH"

RUN git clone $KAVA_GIT_URL && \
    cd kava && \
    git checkout $KAVA_RELEASE && \
    make install COSMOS_BUILD_OPTIONS=rocksdb

RUN mv /go/bin/kava /bin/kava && ldconfig

ENTRYPOINT ["kava"]
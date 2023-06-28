FROM --platform=linux/amd64 ubuntu:22.04 as builder

ARG KAVA_GIT_URL="https://github.com/kava-labs/kava.git"
ARG KAVA_RELEASE="v0.23.3"
ARG ROCKSDB_GIT_URL="https://github.com/facebook/rocksdb.git"
ARG ROCKSDB_RELEASE="v7.10.2"

RUN apt update && \
    apt -y dist-upgrade && \
    DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ \
        make \
        liblz4-dev \
        libgflags-dev \
        libzstd-dev \
        libsnappy-dev \
        zlib1g-dev \
        libbz2-dev \
        git \
        curl \
        tzdata \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /

RUN git clone $ROCKSDB_GIT_URL rocksdb && \
    cd rocksdb && \
    git checkout $ROCKSDB_RELEASE && \
    DISABLE_JEMALLOC=1 make -j$(($(nproc --all)-2)) install-shared && \
    ldconfig

WORKDIR /

RUN curl -LO https://go.dev/dl/go1.20.4.linux-amd64.tar.gz \
    && tar -C /usr/local -xzf go1.20.4.linux-amd64.tar.gz \
    && rm go1.20.4.linux-amd64.tar.gz

ENV GOPATH=/go \
    PATH=$GOPATH/bin:/usr/local/go/bin:$PATH

RUN mkdir -p "$GOPATH/src" "$GOPATH/bin" && chmod -R 777 "$GOPATH"

RUN git clone $KAVA_GIT_URL kava && \
    cd kava && \
    git checkout $KAVA_RELEASE && \
    make install COSMOS_BUILD_OPTIONS=rocksdb

#==============================================================
FROM ubuntu:22.04 as execution

ENV DEBIAN_FRONTEND=noninteractive \
    USERNAME=appuser \
    APP_PATH=/data

RUN apt update && \
    apt -y dist-upgrade && \
    apt install -y --no-install-recommends \
        tzdata \
        libgflags-dev \
        libsnappy-dev \
        nano \
        curl \
        jq \
        ca-certificates && \
    rm -rf /var/cache/apt/*

ARG ROCKSDB_VERSION="7.10.2"  #! no v preffix!!!
COPY --from=builder /usr/local/lib/librocksdb.so.${ROCKSDB_VERSION} /usr/local/lib/
COPY --from=builder /go/bin/* /usr/local/bin/

RUN cd /usr/local/lib && \
    ln -s librocksdb.so.${ROCKSDB_VERSION} librocksdb.so && \
    ln -s librocksdb.so.${ROCKSDB_VERSION} librocksdb.so.7 && \
    ln -s librocksdb.so.${ROCKSDB_VERSION} librocksdb.so.7.10 && \
    ldconfig

RUN groupadd -g 1001 ${USERNAME} \
    && useradd -m -d ${APP_PATH} -u 1001 -g 1001 ${USERNAME}

EXPOSE 8545 8550 8551 8546 30303 30303/udp 30304 30304/udp 8080 9090 6060
VOLUME ${APP_PATH}

WORKDIR ${APP_PATH}
USER ${USERNAME}

ENTRYPOINT ["kava"]

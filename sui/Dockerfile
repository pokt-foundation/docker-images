FROM --platform=linux/amd64 rust:1.65-buster AS builder
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt -y dist-upgrade && \
    apt install -y --no-install-recommends \
        clang \
        ca-certificates && \
    rm -rf /var/cache/apk/*
ARG GIT_URL="https://github.com/MystenLabs/sui.git"
# AUTO_UPDATE_GIT_COMMIT - next line will be overwritten by build.sh to the latest found releas
ARG GIT_COMMIT="devnet-0.15.1"

RUN git clone --depth 1 --branch $GIT_COMMIT $GIT_URL /src
WORKDIR /src
RUN cargo build --release

#==============================================================

FROM --platform=linux/amd64 debian:buster-slim
ENV DEBIAN_FRONTEND=noninteractive
ENV USERNAME=appuser \
    APP_PATH=/data

RUN apt update && \
    apt -y dist-upgrade && \
    apt install -y --no-install-recommends \
        tzdata \
        libjemalloc-dev \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /src/target/release/sui-node /usr/local/bin/

RUN groupadd -g 1001 ${USERNAME} \
    && useradd -m -d ${APP_PATH} -u 1001 -g 1001 ${USERNAME}

# EXPOSE 8545 8550 8551 8546 30303 30303/udp 30304 30304/udp 8080 9090 6060
# VOLUME ${APP_PATH}

WORKDIR ${APP_PATH}
USER ${USERNAME}

ENTRYPOINT ["/usr/local/bin/sui-node"]

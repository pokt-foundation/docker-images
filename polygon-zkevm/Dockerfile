FROM --platform=linux/amd64 golang:bullseye AS builder

ARG GIT_URL="https://github.com/0xPolygonHermez/zkevm-node.git"
# AUTO_UPDATE_GIT_COMMIT - next line will be overwritten by build.sh to the latest found releas
ARG RELEASE="v0.0.7"

#build-base linux-headers git bash ca-certificates libstdc++
RUN apt update && \
    apt -y dist-upgrade && \
    apt install -y --no-install-recommends \
        tzdata \
        ca-certificates \
        make \
        git \
        bash

RUN git clone --depth 1 --branch $RELEASE $GIT_URL /src
WORKDIR /src

# INSTALL DEPENDENCIES
RUN go install github.com/gobuffalo/packr/v2/packr2@v2.8.3 && \
    go mod download

# BUILD BINARY
RUN cd db && \
    packr2 && \
    cd .. && \
    make build

#==============================================================
FROM debian:bullseye-slim as execution

ENV DEBIAN_FRONTEND=noninteractive \
    USERNAME=appuser \
    APP_PATH=/data

RUN apt update && \
    apt -y dist-upgrade && \
    apt install -y --no-install-recommends \
        tzdata \
        ca-certificates && \
    rm -rf /var/cache/apt/*

RUN groupadd -g 1001 ${USERNAME} \
    && useradd -m -d ${APP_PATH} -u 1001 -g 1001 ${USERNAME}

COPY --from=builder /src/dist/zkevm-node /usr/local/bin/zkevm-node
COPY --from=builder /src/config/environments /home/

VOLUME ${APP_PATH}
EXPOSE 8123 8545 9091

WORKDIR ${APP_PATH}
USER ${USERNAME}

ENTRYPOINT ["zkevm-node"]

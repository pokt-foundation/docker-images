FROM golang:1.19.4-bullseye AS build-env

ARG EVMOS_REPO="https://github.com/evmos/evmos.git"
ARG RELEASE="v10.0.1"

RUN apt update && \
    apt install git unzip -y

WORKDIR /go/src/github.com/evmos/evmos
RUN git clone --depth 1 -b ${RELEASE} ${EVMOS_REPO} .

RUN make build

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

COPY --from=build-env /go/src/github.com/evmos/evmos/build/evmosd /usr/local/bin/evmosd

RUN groupadd -g 1001 ${USERNAME} \
    && useradd -m -d ${APP_PATH} -u 1001 -g 1001 ${USERNAME}

VOLUME ${APP_PATH}
WORKDIR ${APP_PATH}
USER ${USERNAME}
EXPOSE 26656 26657 1317 9090

ENTRYPOINT ["evmosd"]

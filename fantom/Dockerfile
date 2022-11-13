FROM golang:bullseye AS build-env

ARG FANTOM_REPO="https://github.com/Fantom-foundation/go-opera.git"
ARG FANTOM_RELEASE="v1.1.1-rc.2"

WORKDIR /go/src/github.com/Fantom-foundation/go-opera

RUN apt update && \
    apt -y dist-upgrade && \
    apt install -y --no-install-recommends git

RUN git clone --depth 1 -b ${FANTOM_RELEASE} ${FANTOM_REPO} .

RUN make
#======================================================

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

COPY --from=build-env /go/src/github.com/Fantom-foundation/go-opera/build/opera /usr/local/bin/opera

RUN groupadd -g 1001 ${USERNAME} \
    && useradd -m -d ${APP_PATH} -u 1001 -g 1001 ${USERNAME}

USER ${USERNAME}

CMD ["opera"]

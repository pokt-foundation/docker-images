# syntax=docker/dockerfile:1-labs
FROM golang:1.19 as op-geth

ENV GIT_URL=https://github.com/ethereum-optimism/op-geth
ENV RELEASE="v1.101200.1"

WORKDIR /app
ADD $GIT_URL/archive/refs/tags/$RELEASE.tar.gz ./
RUN tar -xvf ./$RELEASE.tar.gz --strip-components=1 && \
    go run build/ci.go install -static ./cmd/geth

##################################
FROM debian:12

RUN apt-get update && \
    apt -y dist-upgrade && \
    apt-get install -y jq curl && \
    rm -rf /var/lib/apt/lists

ENV USERNAME=appuser \
    APP_PATH=/data

COPY --from=op-geth --chmod=0755 /app/build/bin/geth /usr/local/bin/

RUN groupadd -g 1001 ${USERNAME} \
    && useradd -m -d ${APP_PATH} -u 1001 -g 1001 ${USERNAME}

WORKDIR ${APP_PATH}
USER ${USERNAME}

ENTRYPOINT ["geth"]

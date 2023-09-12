# syntax=docker/dockerfile:1-labs
############ Build OP_NODE
FROM golang:1.19 as op-node

WORKDIR /app

ENV GIT_URL=https://github.com/ethereum-optimism/optimism
ENV RELEASE="v1.1.4"

ADD $GIT_URL/archive/refs/tags/op-node/$RELEASE.tar.gz ./
RUN tar -xvf ./$RELEASE.tar.gz --strip-components=1 && \
    cd op-node && \
    make op-node

##################################
FROM debian:12

RUN apt-get update && \
    apt -y dist-upgrade && \
    apt-get install -y jq curl && \
    rm -rf /var/lib/apt/lists

ENV USERNAME=appuser \
    APP_PATH=/data

COPY --from=op-node --chmod=0755 /app/op-node/bin/op-node /usr/local/bin/

RUN groupadd -g 1001 ${USERNAME} \
    && useradd -m -d ${APP_PATH} -u 1001 -g 1001 ${USERNAME}

WORKDIR ${APP_PATH}
USER ${USERNAME}

ENTRYPOINT ["op-node"]

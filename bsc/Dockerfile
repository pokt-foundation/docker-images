FROM debian:bullseye-slim

ARG GIT_URL="https://github.com/bnb-chain/bsc"
ARG RELEASE="v1.1.20"

ENV DEBIAN_FRONTEND=noninteractive \
    USERNAME=appuser \
    APP_PATH=/data

RUN apt update && \
    apt -y dist-upgrade && \
    apt install -y --no-install-recommends \
        tzdata \
        unzip \
        ca-certificates && \
    rm -rf /var/cache/apt/*

ADD --chmod=0755 ${GIT_URL}/releases/download/${RELEASE}/geth_linux /usr/local/bin/geth
ADD --chmod=0755 ${GIT_URL}/releases/download/${RELEASE}/mainnet.zip /home
RUN unzip /home/mainnet.zip -d /home && \
    rm /home/mainnet.zip

RUN groupadd -g 1001 ${USERNAME} \
    && useradd -m -d ${APP_PATH} -u 1001 -g 1001 ${USERNAME}

EXPOSE 8545 8550 8551 8546 30303 30303/udp 30304 30304/udp 8080 9090 6060
VOLUME ${APP_PATH}

WORKDIR ${APP_PATH}
USER ${USERNAME}

ENTRYPOINT ["geth"]

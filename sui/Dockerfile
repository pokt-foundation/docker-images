FROM --platform=linux/amd64 debian:bullseye

ARG GIT_URL="https://github.com/MystenLabs/sui"

# AUTO_UPDATE_GIT_COMMIT - next line will be overwritten by build.sh to the latest found releas
ARG RELEASE="sui-v1.0.0"

ENV DEBIAN_FRONTEND=noninteractive
ENV USERNAME=appuser \
    APP_PATH=/data

RUN apt update && \
    apt -y dist-upgrade && \
    apt install -y --no-install-recommends \
        tzdata \
        libjemalloc-dev \
        wget \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN wget -O /usr/local/bin/sui-node ${GIT_URL}/releases/download/${RELEASE}/sui-node && \
    chmod a+x /usr/local/bin/sui-node

RUN groupadd -g 1001 ${USERNAME} \
    && useradd -m -d ${APP_PATH} -u 1001 -g 1001 ${USERNAME}

# EXPOSE 8545 8550 8551 8546 30303 30303/udp 30304 30304/udp 8080 9090 6060
# VOLUME ${APP_PATH}

WORKDIR ${APP_PATH}
USER ${USERNAME}

ENTRYPOINT ["/usr/local/bin/sui-node"]

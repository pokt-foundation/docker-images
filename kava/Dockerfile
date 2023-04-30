FROM --platform=linux/amd64 debian:bookworm-slim
# Requires GLIBC_2.32+ so use bookworm

ARG GIT_URL="https://github.com/Kava-Labs/kava"
# AUTO_UPDATE_GIT_COMMIT - next line will be overwritten by build.sh to the latest found releas
ARG RELEASE="v0.21.1"

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

ADD --chmod=0755 ${GIT_URL}/releases/download/${RELEASE}/kava-${RELEASE}-linux-amd64 /usr/local/bin/kava

RUN groupadd -g 1001 ${USERNAME} \
    && useradd -m -d ${APP_PATH} -u 1001 -g 1001 ${USERNAME}

# EXPOSE 8545 8550 8551 8546 30303 30303/udp 30304 30304/udp 8080 9090 6060

WORKDIR ${APP_PATH}
USER ${USERNAME}

ENTRYPOINT ["kava"]

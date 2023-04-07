FROM --platform=linux/amd64 golang:bullseye AS builder

ARG GIT_URL="https://github.com/maticnetwork/bor.git"
# AUTO_UPDATE_GIT_COMMIT - next line will be overwritten by build.sh to the latest found releas
ARG RELEASE="v0.3.7"

#build-base linux-headers git bash ca-certificates libstdc++
RUN apt update && \
    apt -y dist-upgrade && \
    apt install -y --no-install-recommends \
        tzdata \
        ca-certificates \
        make \
        linux-headers-amd64 \
        git \
        bash

RUN git clone --depth 1 --branch $RELEASE $GIT_URL /src
WORKDIR /src

RUN make bor
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

COPY --from=builder /src/build/bin/* /usr/local/bin/

RUN groupadd -g 1001 ${USERNAME} \
    && useradd -m -d ${APP_PATH} -u 1001 -g 1001 ${USERNAME}

EXPOSE 8545 8546 30303 30303/udp
VOLUME ${APP_PATH}

WORKDIR ${APP_PATH}
USER ${USERNAME}

ENTRYPOINT ["bor"]

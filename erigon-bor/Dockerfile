FROM --platform=linux/amd64 golang:bullseye AS builder

ARG GIT_URL="https://github.com/maticnetwork/erigon.git"
# AUTO_UPDATE_GIT_COMMIT - next line will be overwritten by build.sh to the latest found releas
ARG RELEASE="v0.0.8"

#build-base linux-headers git bash ca-certificates libstdc++
RUN apt update && \
    apt -y dist-upgrade && \
    apt install -y --no-install-recommends \
        build-essential \
        git \
        bash \
        ca-certificates \
        libstdc++6

RUN git clone --depth 1 --branch $RELEASE $GIT_URL /src
WORKDIR /src
RUN git submodule update --init
RUN go mod download
RUN make all
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

EXPOSE 8545 8550 8551 8546 30303 30303/udp 30304 30304/udp 8080 9090 6060
VOLUME ${APP_PATH}

WORKDIR ${APP_PATH}
USER ${USERNAME}

ENTRYPOINT ["erigon"]

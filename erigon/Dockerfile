FROM --platform=linux/amd64 golang:1.19-alpine3.16 AS builder

ARG GIT_URL="https://github.com/ledgerwatch/erigon.git"
# AUTO_UPDATE_GIT_COMMIT - next line will be overwritten by build.sh to the latest found releas
ARG GIT_COMMIT="2022.10.01"

RUN apk --no-cache add make \
                        gcc \
                        g++ \
                        linux-headers \
                        git \
                        bash \
                        ca-certificates \
                        libgcc \
                        libstdc++

RUN git clone --depth 1 --branch $GIT_COMMIT $GIT_URL /src
WORKDIR /src
RUN git submodule update --init
RUN make all
#================================================================

FROM --platform=linux/amd64 alpine:3.16
ENV USERNAME=appuser \
    APP_PATH=/data

RUN apk update && \
    apk upgrade && \
    apk add \
        libgcc \
        libstdc++ \
        tzdata \
        bash \
        curl \
        ca-certificates && \
    rm -rf /var/cache/apk/*

RUN addgroup -g 1001 ${USERNAME} && \
    adduser -G ${USERNAME} -u 1001 -D ${USERNAME}
RUN mkdir -p /home/${USERNAME}/.local/share/erigon
RUN chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}
COPY --from=builder /src/build/bin/* /usr/local/bin/

EXPOSE 8545 8550 8551 8546 30303 30303/udp 30304 30304/udp 8080 9090 6060
VOLUME ${APP_PATH}

WORKDIR ${APP_PATH}
USER ${USERNAME}

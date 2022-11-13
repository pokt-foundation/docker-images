FROM golang:1.19-alpine3.16 AS builder

ARG GIT_URL="https://github.com/maticnetwork/heimdall.git"
ARG GIT_COMMIT="v0.2.12"

RUN apk add --no-cache make gcc musl-dev linux-headers git

ENV GOBIN $GOPATH/bin
RUN cd /root && \
    git clone --depth 1 --branch $GIT_COMMIT $GIT_URL && \
    cd /root/heimdall && \
    make install network=mainnet
#================================================================

FROM alpine:3.16
ENV USERNAME=appuser \
    APP_PATH=/data

RUN apk update && \
    apk upgrade && \
    apk add curl \
            ca-certificates && \
    rm -rf /var/cache/apk/*

RUN addgroup -g 1001 ${USERNAME} && \
    adduser -G ${USERNAME} -u 1001 -D ${USERNAME}

COPY --from=builder /go/bin/ /usr/local/bin/

EXPOSE 1317 26656 26657
VOLUME ${APP_PATH}

WORKDIR ${APP_PATH}
USER ${USERNAME}
ENTRYPOINT ["heimdall"]

FROM golang:1.18-alpine as builder
ARG GIT_URL="https://github.com/scroll-tech/go-ethereum.git"
ARG RELEASE="scroll-v4.3.51"

RUN apk add --no-cache build-base gcc musl-dev linux-headers git

RUN git clone $GIT_URL 

WORKDIR /go/go-ethereum

RUN git checkout $RELEASE

RUN make nccc_geth

##############################
FROM alpine:latest

RUN apk add --no-cache ca-certificates curl

ENV USERNAME=appuser \
    APP_PATH=/data

COPY --from=builder --chmod=0755 /go/go-ethereum/build/bin/geth /usr/local/bin/

RUN addgroup -g 1001 ${USERNAME} \
    && adduser -D -h ${APP_PATH} -u 1001 -G ${USERNAME} ${USERNAME}

WORKDIR ${APP_PATH}
USER ${USERNAME}

ENTRYPOINT ["geth"]





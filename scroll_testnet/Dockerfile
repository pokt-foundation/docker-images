FROM golang:1.18-alpine as builder
ARG GIT_URL="https://github.com/scroll-tech/go-ethereum.git"
ARG RELEASE="scroll-v3.3.1"


RUN apk add --no-cache gcc musl-dev linux-headers git

RUN git clone $GIT_URL 

WORKDIR /go/go-ethereum

RUN git checkout $RELEASE

RUN go run build/ci.go install ./cmd/geth

FROM alpine:latest

RUN apk add --no-cache ca-certificates
COPY --from=builder /go/go-ethereum/build/bin/geth /usr/local/bin/

EXPOSE 8545 8546 30303 30303/udp
ENTRYPOINT ["geth"]





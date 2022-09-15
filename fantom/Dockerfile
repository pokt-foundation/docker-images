FROM golang:1.18.5-buster AS build-env

ARG FANTOM_REPO="https://github.com/Fantom-foundation/go-opera.git"
ARG FANTOM_RELEASE="v1.1.1-rc.2"

WORKDIR /go/src/github.com/Fantom-foundation/go-opera

RUN apt update
RUN apt install git -y

RUN git clone --depth 1 -b ${FANTOM_RELEASE} ${FANTOM_REPO} .

RUN make

FROM debian:buster-slim as execution

COPY --from=build-env /go/src/github.com/Fantom-foundation/go-opera/build/opera /usr/bin/opera

CMD ["opera"]

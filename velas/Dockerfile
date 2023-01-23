FROM --platform=linux/amd64 debian:bullseye

ARG RELEASE="v0.6.3"

WORKDIR /root

RUN apt-get update && apt-get install -y wget lbzip2 \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/velas/velas-chain/releases/download/${RELEASE}/velas-release-x86_64-unknown-linux-gnu.tar.bz2 \
    && tar -xvf velas-release-x86_64-unknown-linux-gnu.tar.bz2 \
    && cd velas-release \
    && chmod -R +x bin/ \
    && mv bin/* /usr/bin/

ENTRYPOINT ["velas-validator"]
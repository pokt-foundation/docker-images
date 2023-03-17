FROM debian:bullseye

ARG RELEASE="v1.0.5"

RUN apt update  \
    && apt install -y --no-install-recommends unzip wget ca-certificates 
    
WORKDIR /data

RUN useradd -s /sbin/nologin geth \
    && chown geth:geth /data \
    && chmod 700 /data


RUN wget https://github.com/oasysgames/oasys-validator/releases/download/${RELEASE}/geth-v1.0.4-linux-amd64.zip \
    && unzip geth-v1.0.4-linux-amd64.zip \
    && rm geth-v1.0.4-linux-amd64.zip \
    && mv geth /usr/local/bin/ \
    && chmod +x /usr/local/bin/geth 


RUN wget https://github.com/oasysgames/oasys-validator/releases/download/${RELEASE}/genesis.zip \
    && unzip genesis.zip  \
    && rm genesis.zip \
    && mv genesis/mainnet.json /data/genesis.json \
    && rm -r genesis


EXPOSE 30301 30301/udp 8545

CMD ["-u geth geth"] 
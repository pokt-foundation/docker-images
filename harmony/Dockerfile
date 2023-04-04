FROM alpine:3.15

ARG RELEASE="v2013.1.3"

RUN apk add --no-cache bash curl libstdc++ gmp-dev libc6-compat bind-tools jq && ln -s libcrypto.so.1.1 /lib/libcrypto.so.10

EXPOSE 9000/tcp 9500/tcp 9800/tcp 6000/tcp

ENV NODE_BN_MNET "/ip4/100.26.90.187/tcp/9874/p2p/Qmdfjtk6hPoyrH1zVD9PEH4zfWLo38dP2mDvvKXfh3tnEv,/ip4/54.213.43.194/tcp/9874/p2p/QmZJJx6AdaoEkGLrYG4JeLCKeCKDjnFz2wfHNHxAqFSGA9,/ip4/13.113.101.219/tcp/12019/p2p/QmQayinFSgMMw5cSpDUiD9pQ2WeP6WNmGxpZ6ou3mdVFJX,/ip4/99.81.170.167/tcp/12019/p2p/QmRVbTpEYup8dSaURZfF6ByrMTSKa4UyUzJhSjahFzRqNj"

ENV NODE_PORT "9000"
ENV NODE_BLSKEY ""
ENV NODE_BLSPASS ""
ENV NODE_DNS_ZONE "t.hmny.io"
ENV NODE_RPC "true"
ENV NODE_BLACKLIST ""
ENV NODE_NETWORK_TYPE "mainnet"

WORKDIR /harmony

RUN curl -LO https://github.com/harmony-one/harmony/releases/download/${RELEASE}/harmony
RUN mv harmony /bin/harmony
RUN chmod +x /bin/harmony

ENTRYPOINT ["/bin/harmony"]

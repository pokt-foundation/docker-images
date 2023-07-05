FROM debian:bookworm-slim

ARG GIT_URL="https://github.com/gohugoio/hugo"
# AUTO_UPDATE_GIT_COMMIT - next line will be overwritten by build.sh to the latest found releas
ARG VERSION="0.115.1"

ENV DEBIAN_FRONTEND=noninteractive \
    USERNAME=appuser \
    APP_PATH=/data

RUN apt update && \
    apt -y dist-upgrade && \
    apt install -y --no-install-recommends \
        tzdata \
        curl \
        git \
        ca-certificates && \
    rm -rf /var/cache/apt/*

RUN curl -L -o /tmp/hugo_${VERSION}_linux-amd64.deb ${GIT_URL}/releases/download/v${VERSION}/hugo_${VERSION}_linux-amd64.deb && \
    apt install -fy /tmp/hugo_${VERSION}_linux-amd64.deb

RUN groupadd -g 1001 ${USERNAME} \
    && useradd -m -d ${APP_PATH} -u 1001 -g 1001 ${USERNAME}

EXPOSE 1313

VOLUME ${APP_PATH}
WORKDIR ${APP_PATH}
USER ${USERNAME}

ENTRYPOINT ["hugo"]

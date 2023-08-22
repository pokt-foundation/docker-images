FROM php:8.2-apache

ARG GLPI_REPO="https://github.com/glpi-project/glpi"
ARG GLPI_RELEASE="10.0.9"
ENV GLPI_DIR=/var/www/html

# Install GLPI
WORKDIR $GLPI_DIR
ADD ${GLPI_REPO}/releases/download/${GLPI_RELEASE}/glpi-${GLPI_RELEASE}.tgz ./
RUN tar -xvf glpi-${GLPI_RELEASE}.tgz --strip-components=1 && \
    rm glpi-${GLPI_RELEASE}.tgz
#     && \
#    mv ./config $GLPI_CONFIG_DIR && \
#    mv ./files $GLPI_VAR_DIR


COPY php/php.ini /usr/local/etc/php/php.ini
COPY apache /etc/apache2/sites-enabled

RUN apt update && \
    apt -y dist-upgrade && \
    apt install -y --no-install-recommends \
        tzdata \
        ca-certificates \
        curl \
        sendmail \
        libpng-dev \
        libldap2-dev \
        zlib1g-dev \
        libicu-dev \
        libzip-dev \
        libbz2-dev && \
    rm -rf /var/cache/apt/*

RUN docker-php-ext-install mysqli && \
    docker-php-ext-install gd && \
    docker-php-ext-install intl && \
    docker-php-ext-install exif && \
    docker-php-ext-install ldap && \
    docker-php-ext-install zip && \
    docker-php-ext-install bz2 && \
    docker-php-ext-install opcache

RUN useradd -ms /bin/bash admin

RUN chown -R admin:admin /var/www/html

USER admin

VOLUME [/var/www/html]

EXPOSE 8080/tcp

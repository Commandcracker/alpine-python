ARG ALPINE_VERSION

FROM alpine:${ALPINE_VERSION}

RUN set -eux; \
    repositories="$(cat /etc/apk/repositories)"; \
    echo "https://dl-cdn.alpinelinux.org/alpine/v3.15/community" >> /etc/apk/repositories; \
    apk add --no-cache python2; \
    echo "$repositories" > /etc/apk/repositories;

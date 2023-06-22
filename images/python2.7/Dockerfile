ARG ALPINE_VERSION

FROM alpine:${ALPINE_VERSION} AS builder

ADD cve-2021-3177.patch /tmp/python2/cve-2021-3177.patch
ADD musl-find_library.patch /tmp/python2/musl-find_library.patch
ADD unchecked-ioctl.patch /tmp/python2/unchecked-ioctl.patch

ENV \
    PYTHON_VERSION=2.7.18 \
    PYTHON_SHA512SUM="a7bb62b51f48ff0b6df0b18f5b0312a523e3110f49c3237936bfe56ed0e26838c0274ff5401bda6fc21bf24337477ccac49e8026c5d651e4b4cafb5eb5086f6c python.tar.xz"

WORKDIR /tmp/python2

RUN set -eux; \
    apk add --no-cache \
    expat-dev \
    openssl1.1-compat-dev \
    zlib-dev \
    ncurses-dev \
    bzip2-dev \
    gdbm-dev \
    sqlite-dev \
    libffi-dev \
    readline-dev \
    linux-headers \
    curl \
    make \
    build-base \
    patch; \
    curl --silent --location https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz --output python.tar.xz; \
    echo ${PYTHON_SHA512SUM} | sha512sum -c -; \
    tar -xf python.tar.xz; \
    patch --binary -p0 < /tmp/python2/cve-2021-3177.patch; \
    patch --binary -p0 < /tmp/python2/musl-find_library.patch; \
    cd Python-${PYTHON_VERSION}; \
    patch --binary -p0 < /tmp/python2/unchecked-ioctl.patch; \
    ./configure \
    --prefix=/usr \
    --enable-ipv6 \
    --enable-optimizations \
    --enable-shared \
    --enable-unicode=ucs4 \
    --with-system-expat \
    --with-system-ffi \
    --with-system-zlib \
    --with-threads; \
    make; \
    make install

FROM alpine:${ALPINE_VERSION} 

COPY --from=builder /usr/lib /usr/lib
COPY --from=builder /usr/bin /usr/bin

RUN set -eux; \
    apk add --no-cache \
    expat \
    gdbm \
    libbz2 \
    libcrypto1.1 \
    libffi \
    libssl1.1 \
    musl \
    ncurses-libs \
    readline \
    sqlite-libs \
    zlib

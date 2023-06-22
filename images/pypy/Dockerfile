ARG BASE_IMAGE
ARG ALPINE_VERSION

FROM ${BASE_IMAGE} as builder

ARG \
	PYTHON_VERSION \
	PYPY_VERSION \
	PYPY_SHA256SUM

RUN set -eux; \
	apk add --no-cache \
	bzip2-dev \
	expat-dev \
	gdbm-dev \
	libc-dev \
	libffi-dev \
	linux-headers \
	ncurses-dev \
	openssl-dev>3 \
	perl \
	pkgconf \
	readline-dev \
	rsync \
	sqlite-dev \
	tk-dev \
	xz-dev \
	zlib-dev \
	# for pypy/rpython/bin/rpython
	gcc \
	make \
	# for pypy/tool/release/package.py
	tar; \
	# download pypy
	wget -O pypy.tar.bz2 "https://foss.heptapod.net/pypy/pypy/-/archive/release-pypy${PYTHON_VERSION}-v${PYPY_VERSION}/pypy-release-pypy${PYTHON_VERSION}-v${PYPY_VERSION}.tar.bz2"; \
	echo "$PYPY_SHA256SUM pypy.tar.bz2" | sha256sum -c -; \
	mkdir -p /opt/pypy_src; \
	tar -xjC /opt/pypy_src --strip-components=1 -f pypy.tar.bz2; \
	rm pypy.tar.bz2; \
	# build pypy
	cd /opt/pypy_src/pypy/goal; \
	python2 ../../rpython/bin/rpython --opt=jit; \
	python2 /opt/pypy_src/pypy/tool/release/package.py --archive-name pypy --builddir /opt/pypy_build

FROM alpine:${ALPINE_VERSION}

RUN set -eux; \
	apk add --no-cache \
	gdbm \
	libbz2 \
	libcrypto3 \
	libexpat \
	libffi \
	libssl3 \
	musl \
	ncurses-libs \
	sqlite-libs \
	tcl \
	tk \
	zlib \
	libgcc

ENV PATH /opt/pypy/bin:$PATH

COPY --from=builder /opt/pypy_build/pypy /opt/pypy

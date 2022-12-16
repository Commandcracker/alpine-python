FROM alpine-pypy2-pycparser:3.17.0 as builder

ENV \
	PYTHON_VERSION=3.9 \
	PYPY_VERSION=7.3.10 \
	PYPY_SHA256SUM=241f5a22cd2e5eb8a80d41f5c449e6c5978a144390e1e22679a35a30ce328f6c

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
	echo "$PYPY_SHA256SUM *pypy.tar.bz2" | sha256sum -c -; \
	mkdir -p /opt/pypy_src; \
	tar -xjC /opt/pypy_src --strip-components=1 -f pypy.tar.bz2; \
	rm pypy.tar.bz2; \
	# build pypy
	cd /opt/pypy_src/pypy/goal; \
	if which pypy&>/dev/null;then RUNINTERP=pypy;else RUNINTERP=python;fi; \
	$RUNINTERP ../../rpython/bin/rpython --opt=jit; \
	$RUNINTERP /opt/pypy_src/pypy/tool/release/package.py --archive-name pypy --builddir /opt/pypy_build

FROM alpine:3.17.0

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

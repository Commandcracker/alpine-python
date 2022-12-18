ARG BASE_IMAGE

FROM ${BASE_IMAGE}

ARG \
    PIP_WHL \
    PIP_SHA256 \
    PIP_URL

RUN set -eux; \
    wget -O ${PIP_WHL} ${PIP_URL}; \
    echo "${PIP_SHA256} *${PIP_WHL}" | sha256sum -c -; \
    python ${PIP_WHL}/pip install --no-index ${PIP_WHL}; \
    rm ${PIP_WHL}

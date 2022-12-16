FROM alpine-pypy3.9:3.17.0

RUN set -eux; \
    wget -O pip-22.3.1-py3-none-any.whl "https://files.pythonhosted.org/packages/09/bd/2410905c76ee14c62baf69e3f4aa780226c1bbfc9485731ad018e35b0cb5/pip-22.3.1-py3-none-any.whl"; \
    echo "908c78e6bc29b676ede1c4d57981d490cb892eb45cd8c214ab6298125119e077 *pip-22.3.1-py3-none-any.whl" | sha256sum -c -; \
    python pip-22.3.1-py3-none-any.whl/pip install --no-index pip-22.3.1-py3-none-any.whl; \
    rm pip-22.3.1-py3-none-any.whl

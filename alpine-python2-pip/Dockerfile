FROM alpine-python2:3.17.0

RUN set -eux; \
    wget -O pip-20.3.4-py2.py3-none-any.whl "https://files.pythonhosted.org/packages/27/79/8a850fe3496446ff0d584327ae44e7500daf6764ca1a382d2d02789accf7/pip-20.3.4-py2.py3-none-any.whl"; \
    echo "217ae5161a0e08c0fb873858806e3478c9775caffce5168b50ec885e358c199d *pip-20.3.4-py2.py3-none-any.whl" | sha256sum -c -; \
    python2 pip-20.3.4-py2.py3-none-any.whl/pip install --no-index pip-20.3.4-py2.py3-none-any.whl; \
    rm pip-20.3.4-py2.py3-none-any.whl

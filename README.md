# alpine-python

Python docker images for Alpine Linux

## Images

|               | python2.7                    | pypy2.7                    | pypy3.8              | pypy3.9              | pypy3.10              |
|---------------|------------------------------|----------------------------|----------------------|----------------------|-----------------------|
| **python**    | [alpine-python2.7]           | [alpine-pypy2.7]           | [alpine-pypy3.8]     | [alpine-pypy3.9]     | [alpine-pypy3.10]     |
| **pip**       | [alpine-python2.7-pip]       | [alpine-pypy2.7-pip]       | [alpine-pypy3.8-pip] | [alpine-pypy3.9-pip] | [alpine-pypy3.10-pip] |
| **pycparser** | [alpine-python2.7-pycparser] | [alpine-pypy2.7-pycparser] |                      |                      |                       |

[alpine-python2.7]: https://github.com/Commandcracker/alpine-python/pkgs/container/alpine-python2.7
[alpine-python2.7-pip]: https://github.com/Commandcracker/alpine-python/pkgs/container/alpine-python2.7-pip
[alpine-python2.7-pycparser]: https://github.com/Commandcracker/alpine-python/pkgs/container/alpine-python2.7-pycparser
[alpine-pypy2.7]: https://github.com/Commandcracker/alpine-python/pkgs/container/alpine-pypy2.7
[alpine-pypy2.7-pip]: https://github.com/Commandcracker/alpine-python/pkgs/container/alpine-pypy2.7-pip
[alpine-pypy2.7-pycparser]: https://github.com/Commandcracker/alpine-python/pkgs/container/alpine-pypy2.7-pycparser
[alpine-pypy3.8]: https://github.com/Commandcracker/alpine-python/pkgs/container/alpine-pypy3.8
[alpine-pypy3.8-pip]: https://github.com/Commandcracker/alpine-python/pkgs/container/alpine-pypy3.8-pip
[alpine-pypy3.9]: https://github.com/Commandcracker/alpine-python/pkgs/container/alpine-pypy3.9
[alpine-pypy3.9-pip]: https://github.com/Commandcracker/alpine-python/pkgs/container/alpine-pypy3.9-pip
[alpine-pypy3.10]: https://github.com/Commandcracker/alpine-python/pkgs/container/alpine-pypy3.10
[alpine-pypy3.10-pip]: https://github.com/Commandcracker/alpine-python/pkgs/container/alpine-pypy3.10-pip

## Tags

| \*                  | pypy-\*                                  | pip-\*                                 | pypy-\*-pip-\*                                              | pycparser-\*                                       | pypy-\*-pycparser-\*                                                    |
|---------------------|------------------------------------------|----------------------------------------|-------------------------------------------------------------|----------------------------------------------------|-------------------------------------------------------------------------|
| `latest`            | `pypy-${PYPY_VERSION}`                   | `pip-${PIP_VERSION}`                   | `pypy-${PYPY_VERSION}-pip-${PIP_VERSION}`                   | `pycparser-${PYCPARSER_VERSION}`                   | `pypy-${PYPY_VERSION}-pycparser-${PYCPARSER_VERSION}`                   |
| `${ALPINE_VERSION}` | `${ALPINE_VERSION}-pypy-${PYPY_VERSION}` | `${ALPINE_VERSION}-pip-${PIP_VERSION}` | `${ALPINE_VERSION}-pypy-${PYPY_VERSION}-pip-${PIP_VERSION}` | `${ALPINE_VERSION}-pycparser-${PYCPARSER_VERSION}` | `${ALPINE_VERSION}-pypy-${PYPY_VERSION}-pycparser-${PYCPARSER_VERSION}` |

| ALPINE_VERSION | PYPY_VERSION | PYCPARSER_VERSION | PIP_VERSION |
|----------------|--------------|-------------------|-------------|
| [alpine]       | [pypy]       | [pycparser]       | [pip]       |

[alpine]: https://hub.docker.com/_/alpine/
[pypy]: https://foss.heptapod.net/pypy/pypy/
[pycparser]: https://pypi.org/project/pycparser/
[pip]: https://pypi.org/project/pip/

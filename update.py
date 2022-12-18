from json import loads
from urllib.request import urlopen
from re import (
    compile as re_compile,
    search as re_search
)
from hashlib import sha256


def http_get_dict(url: str) -> dict:
    return loads(urlopen(url, timeout=10).read())


def get_latest_alpine() -> str:
    data = http_get_dict(
        "https://hub.docker.com/v2/repositories/library/alpine/tags/?page_size=25&page=1"
    )

    latest_digest = None
    for image in data.get("results"):
        if image.get("name") == "latest":
            latest_digest = image.get("digest")
            break

    if latest_digest is None:
        exit("Faild to get latest alpine version")

    version = None
    for image in data.get("results"):
        if len(image.get("name").split(".")) == 3:
            if image.get("digest") == latest_digest:
                version = image.get("name")
                break

    if version is None:
        exit("Faild to get latest alpine version")

    return version


def get_latest_pip() -> dict:
    data = http_get_dict("https://pypi.org/pypi/pip/json")

    version = data.get("info").get("version")

    for package in data.get("releases").get(version):
        if package.get("packagetype") == "bdist_wheel":
            return {
                "version": version,
                "url": package.get("url"),
                "sha256": package.get("digests").get("sha256"),
                "filename": package.get("filename")
            }

    exit("Faild to get latest pip version")


def get_latest_pypy() -> dict:
    data = http_get_dict(
        "https://foss.heptapod.net/api/v4/projects/76/repository/tags")

    tag_list = []
    for tag in data:
        tag_list.append(tag.get("name"))

    tags = "\n".join(tag_list)
    version_pattern = re_compile(
        r"release-pypy\d\.\d-v(?P<version>\d*\.\d*\.\d*)"
    )

    result = re_search(version_pattern, tags)
    groups = result.groupdict()

    if groups.get("version") is None:
        exit("Faild to get latest pypy version")

    return groups.get("version")


def get_pypy_archive_sha256(python_version: str, pypy_version: str):
    return sha256(
        urlopen(
            f"https://foss.heptapod.net/pypy/pypy/-/archive/release-pypy{python_version}-v{pypy_version}/pypy-release-pypy{python_version}-v{pypy_version}.tar.bz2",
            timeout=20
        ).read()
    ).hexdigest()


def main() -> None:
    latest_pip = get_latest_pip()
    latest_pypy = get_latest_pypy()
    print(f"""
ALPINE_VERSION = "{get_latest_alpine()}"

pypy_version = "{latest_pypy}"
pypy2_7_sha256 = "{get_pypy_archive_sha256("2.7", latest_pypy)}"
pypy3_8_sha256 = "{get_pypy_archive_sha256("3.8", latest_pypy)}"
pypy3_9_sha256 = "{get_pypy_archive_sha256("3.9", latest_pypy)}"

python2_pip_version = "20.3.4"
python2_pip_sha256 = "217ae5161a0e08c0fb873858806e3478c9775caffce5168b50ec885e358c199d"
python2_pip_whl_name = "pip-20.3.4-py2.py3-none-any.whl"
python2_pip_downlaod_url = "https://files.pythonhosted.org/packages/27/79/8a850fe3496446ff0d584327ae44e7500daf6764ca1a382d2d02789accf7/pip-20.3.4-py2.py3-none-any.whl"

python3_pip_version = "{latest_pip.get("version")}"
python3_pip_sha256 = "{latest_pip.get("sha256")}"
python3_pip_whl_name = "{latest_pip.get("filename")}"
python3_pip_downlaod_url = "{latest_pip.get("url")}"

pycparser_version = "2.21"
pycparser_whl_name = "pycparser-2.21-py2.py3-none-any.whl"
pycparser_sha256 = "8ee45429555515e1f6b185e78100aea234072576aa43ab53aefcae078162fca9"
pycparser_downlaod_url = "https://files.pythonhosted.org/packages/62/d5/5f610ebe421e85889f2e55e33b7f9a6795bd982198517d912eb1c76e1a53/pycparser-2.21-py2.py3-none-any.whl"
""")


if __name__ == "__main__":
    main()

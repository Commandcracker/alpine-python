
#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import system, chdir, getcwd
from os.path import join
from os import getenv


CWD = getcwd()


class Command(list):
    def __init__(self, *args) -> None:
        super().__init__([*args])

    def run(self, prefix: str = "", suffix: str = "") -> None:
        command = f"{prefix}{self}{suffix}"
        print(
            Colours.Foreground.BRIGHT_BLACK +
            "Runnig command: \"" +
            command + "\"" +
            Colours.RESET,
            flush=True
        )
        system(command)

    def add(self, *args: str) -> None:
        super().extend(args)

    def __repr__(self) -> str:
        return "{}({})".format(self.__class__.__name__, list.__repr__(self)[1:-1])

    def __str__(self) -> str:
        return " ".join(self)


class BuildCommand(Command):
    def __init__(self, path: str) -> None:
        self.path = path
        super().__init__("docker", "build")

    def run(self) -> None:
        chdir(join(CWD, self.path))
        super().run(suffix=" .")

    def add_tag(self, tag: str) -> None:
        self.add("--tag", tag)

    def add_arg(self, key: str, value: str) -> None:
        self.add("--build-arg", f"{key}={value}")

    def add_args(self, args: dict) -> None:
        for key, value in args.items():
            self.add_arg(key, value)


class PushCommand(Command):
    def __init__(self, *args: str) -> None:
        super().__init__("docker", "push", *args)


class MultiPush:
    def __init__(self) -> None:
        self.images = []

    def add(self, image: str) -> None:
        self.images.append(image)

    def run(self) -> None:
        for image in self.images:
            PushCommand(image).run()


class Image:
    def __init__(self, name: str, path: str, remotes: list = None) -> None:
        self.tags = []
        self.name = name
        self.path = path
        self.args = {}
        self.remotes = remotes

    def add_tag(self, tag):
        self.tags.append(tag)

    def add_arg(self, key: str, value: str) -> None:
        self.args[key] = value

    def build(self):
        build_command = BuildCommand(self.path)

        for tag in self.tags:
            build_command.add_tag(f"{self.name}:{tag}")

        build_command.add_args(self.args)

        if self.remotes is not None:
            for remote in self.remotes:
                for tag in self.tags:
                    build_command.add_tag(f"{remote}/{self.name}:{tag}")

        build_command.run()

    def push(self):
        multi_push = MultiPush()

        for tag in self.tags:
            multi_push.add(f"{self.name}:{tag}")

        if self.remotes is not None:
            for remote in self.remotes:
                for tag in self.tags:
                    multi_push.add(f"{remote}/{self.name}:{tag}")

        multi_push.run()


class Colours:
    """
    Colors using ANSI escape codes
    https://en.wikipedia.org/wiki/ANSI_escape_code
    """

    class Foreground:
        """
        [3-bit and 4-bit](https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and_4-bit)
        """
        BLACK = "\033[30m"
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"
        MAGENTA = "\033[35m"
        CYAN = "\033[36m"
        WHITE = "\033[37m"

        BRIGHT_BLACK = "\033[90m"
        BRIGHT_RED = "\033[91m"
        BRIGHT_GREEN = "\033[92m"
        BRIGHT_YELLOW = "\033[93m"
        BRIGHT_BLUE = "\033[94m"
        BRIGHT_MAGENTA = "\033[95m"
        BRIGHT_CYAN = "\033[96m"
        BRIGHT_WHITE = "\033[97m"

        DEFAULT = "\033[39m"

    RESET = "\033[m"


def print_tags(name: str, tags: list) -> None:
    _tags = []
    for tag in tags:
        _tags.append(f"{name}:{tag}")

    length = len(max(_tags, key=len))

    print(
        Colours.Foreground.GREEN + "Tags:" + Colours.RESET + "\n" +
        Colours.Foreground.GREEN + ("-"*length) + Colours.RESET + "\n" +
        Colours.Foreground.GREEN + ("\n" + Colours.Foreground.GREEN).join(_tags) + Colours.RESET + "\n" +
        Colours.Foreground.GREEN + ("-"*length) + Colours.RESET,
        flush=True
    )


def print_banner(message: str) -> None:
    seperator_count = len(message) + 2

    print(
        Colours.Foreground.MAGENTA + ("="*seperator_count) + Colours.RESET + "\n" +
        Colours.Foreground.MAGENTA + " " + message + Colours.RESET + "\n" +
        Colours.Foreground.MAGENTA + ("="*seperator_count) + Colours.RESET,
        flush=True
    )


def main() -> None:
    REGISTRY = getenv("REGISTRY", "ghcr.io")
    REPOSITORY_OWNER = getenv(
        "GITHUB_REPOSITORY_OWNER",
        "commandcracker"
    ).lower()

    ALPINE_VERSION = "3.18.2"

    pypy_version = "7.3.12"
    pypy2_7_sha256 = "75cf675248d0b09bab4de8fc237ee2489f3f8caee77b0e3ef530cf4aac03d445"
    pypy3_8_sha256 = "35786fd68e58330a888adc4c1edc65f4d67d47d21cf090bad406196403f4adcf"
    pypy3_9_sha256 = "52857411c710cd9aced93687cf53f5cfada18cb2a4c43ffa4c83ef27c7a3b58e"
    pypy3_10_sha256 = "3a8cca1d37c2bcfcb788ed06cdda414e78748034c04b0dfd42e239fc0e4edcbb"

    python2_pip_version = "20.3.4"
    python2_pip_sha256 = "217ae5161a0e08c0fb873858806e3478c9775caffce5168b50ec885e358c199d"
    python2_pip_whl_name = "pip-20.3.4-py2.py3-none-any.whl"
    python2_pip_downlaod_url = "https://files.pythonhosted.org/packages/27/79/8a850fe3496446ff0d584327ae44e7500daf6764ca1a382d2d02789accf7/pip-20.3.4-py2.py3-none-any.whl"

    python3_pip_version = "23.1.2"
    python3_pip_sha256 = "3ef6ac33239e4027d9a5598a381b9d30880a1477e50039db2eac6e8a8f6d1b18"
    python3_pip_whl_name = "pip-23.1.2-py3-none-any.whl"
    python3_pip_downlaod_url = "https://files.pythonhosted.org/packages/08/e3/57d4c24a050aa0bcca46b2920bff40847db79535dc78141eb83581a52eb8/pip-23.1.2-py3-none-any.whl"

    pycparser_version = "2.21"
    pycparser_whl_name = "pycparser-2.21-py2.py3-none-any.whl"
    pycparser_sha256 = "8ee45429555515e1f6b185e78100aea234072576aa43ab53aefcae078162fca9"
    pycparser_downlaod_url = "https://files.pythonhosted.org/packages/62/d5/5f610ebe421e85889f2e55e33b7f9a6795bd982198517d912eb1c76e1a53/pycparser-2.21-py2.py3-none-any.whl"

    iamges = {
        # alpine-python2
        "alpine-python2.7": {
            "path": "images/python2.7",
            "args": {
                "ALPINE_VERSION": ALPINE_VERSION
            }
        },
        "alpine-python2.7-pip": {
            "path": "images/pip",
            "args": {
                "BASE_IMAGE": "alpine-python2.7",
                "PIP_WHL": python2_pip_whl_name,
                "PIP_SHA256": python2_pip_sha256,
                "PIP_URL": python2_pip_downlaod_url
            },
            "tags": [
                f"pip-{python2_pip_version}",
                f"{ALPINE_VERSION}-pip-{python2_pip_version}"
            ]
        },
        "alpine-python2.7-pycparser": {
            "path": "images/whl",
            "args": {
                "BASE_IMAGE": "alpine-python2.7",
                "PIP_WHL": python2_pip_whl_name,
                "PIP_SHA256": python2_pip_sha256,
                "PIP_URL": python2_pip_downlaod_url,
                "WHL_WHL": pycparser_whl_name,
                "WHL_SHA256": pycparser_sha256,
                "WHL_URL": pycparser_downlaod_url
            },
            "tags": [
                f"pycparser-{pycparser_version}",
                f"{ALPINE_VERSION}-pycparser-{pycparser_version}"
            ]
        },
        # pypy2.7
        "alpine-pypy2.7": {
            "path": "images/pypy",
            "args": {
                "BASE_IMAGE": "alpine-python2.7-pycparser",
                "PYTHON_VERSION": "2.7",
                "PYPY_VERSION": pypy_version,
                "PYPY_SHA256SUM": pypy2_7_sha256,
                "ALPINE_VERSION": ALPINE_VERSION
            },
            "tags": [
                f"pypy-{pypy_version}",
                f"{ALPINE_VERSION}-pypy-{pypy_version}"
            ]
        },
        "alpine-pypy2.7-pip": {
            "path": "images/pip",
            "args": {
                "BASE_IMAGE": "alpine-pypy2.7",
                "PIP_WHL": python2_pip_whl_name,
                "PIP_SHA256": python2_pip_sha256,
                "PIP_URL": python2_pip_downlaod_url
            },
            "tags": [
                f"pip-{python2_pip_version}",
                f"{ALPINE_VERSION}-pip-{python2_pip_version}",
                f"pypy-{pypy_version}",
                f"{ALPINE_VERSION}-pypy-{pypy_version}",
                f"pypy-{pypy_version}-pip-{python2_pip_version}",
                f"{ALPINE_VERSION}-pypy-{pypy_version}-pip-{python2_pip_version}"
            ]
        },
        "alpine-pypy2.7-pycparser": {
            "path": "images/whl",
            "args": {
                "BASE_IMAGE": "alpine-pypy2.7",
                "PIP_WHL": python2_pip_whl_name,
                "PIP_SHA256": python2_pip_sha256,
                "PIP_URL": python2_pip_downlaod_url,
                "WHL_WHL": pycparser_whl_name,
                "WHL_SHA256": pycparser_sha256,
                "WHL_URL": pycparser_downlaod_url
            },
            "tags": [
                f"pycparser-{pycparser_version}",
                f"{ALPINE_VERSION}-pycparser-{pycparser_version}",
                f"pypy-{pypy_version}",
                f"{ALPINE_VERSION}-pypy-{pypy_version}",
                f"pypy-{pypy_version}-pycparser-{pycparser_version}",
                f"{ALPINE_VERSION}-pypy-{pypy_version}-pycparser-{pycparser_version}"
            ]
        },
        # pypy3.8
        "alpine-pypy3.8": {
            "path": "images/pypy",
            "args": {
                "BASE_IMAGE": "alpine-pypy2.7-pycparser",
                "PYTHON_VERSION": "3.8",
                "PYPY_VERSION": "7.3.11",
                "PYPY_SHA256SUM": pypy3_8_sha256,
                "ALPINE_VERSION": ALPINE_VERSION
            },
            "tags": [
                "pypy-7.3.11",
                f"{ALPINE_VERSION}-pypy-7.3.11"
            ]
        },
        "alpine-pypy3.8-pip": {
            "path": "images/pip",
            "args": {
                "BASE_IMAGE": "alpine-pypy3.8",
                "PIP_WHL": python3_pip_whl_name,
                "PIP_SHA256": python3_pip_sha256,
                "PIP_URL": python3_pip_downlaod_url
            },
            "tags": [
                f"pip-{python3_pip_version}",
                f"{ALPINE_VERSION}-pip-{python3_pip_version}",
                "pypy-7.3.11",
                f"{ALPINE_VERSION}-pypy-7.3.11",
                f"pypy-7.3.11-pip-{python3_pip_version}",
                f"{ALPINE_VERSION}-pypy-7.3.11-pip-{python3_pip_version}"
            ]
        },
        # pypy3.9
        "alpine-pypy3.9": {
            "path": "images/pypy",
            "args": {
                "BASE_IMAGE": "alpine-pypy2.7-pycparser",
                "PYTHON_VERSION": "3.9",
                "PYPY_VERSION": pypy_version,
                "PYPY_SHA256SUM": pypy3_9_sha256,
                "ALPINE_VERSION": ALPINE_VERSION
            },
            "tags": [
                f"pypy-{pypy_version}",
                f"{ALPINE_VERSION}-pypy-{pypy_version}"
            ]
        },
        "alpine-pypy3.9-pip": {
            "path": "images/pip",
            "args": {
                "BASE_IMAGE": "alpine-pypy3.9",
                "PIP_WHL": python3_pip_whl_name,
                "PIP_SHA256": python3_pip_sha256,
                "PIP_URL": python3_pip_downlaod_url
            },
            "tags": [
                f"pip-{python3_pip_version}",
                f"{ALPINE_VERSION}-pip-{python3_pip_version}",
                f"pypy-{pypy_version}",
                f"{ALPINE_VERSION}-pypy-{pypy_version}",
                f"pypy-{pypy_version}-pip-{python3_pip_version}",
                f"{ALPINE_VERSION}-pypy-{pypy_version}-pip-{python3_pip_version}"
            ]
        },
        # alpine-pypy3.10
        "alpine-pypy3.10": {
            "path": "images/pypy",
            "args": {
                "BASE_IMAGE": "alpine-pypy2.7-pycparser",
                "PYTHON_VERSION": "3.10",
                "PYPY_VERSION": pypy_version,
                "PYPY_SHA256SUM": pypy3_10_sha256,
                "ALPINE_VERSION": ALPINE_VERSION
            },
            "tags": [
                f"pypy-{pypy_version}",
                f"{ALPINE_VERSION}-pypy-{pypy_version}"
            ]
        },
        "alpine-pypy3.10-pip": {
            "path": "images/pip",
            "args": {
                "BASE_IMAGE": "alpine-pypy3.10",
                "PIP_WHL": python3_pip_whl_name,
                "PIP_SHA256": python3_pip_sha256,
                "PIP_URL": python3_pip_downlaod_url
            },
            "tags": [
                f"pip-{python3_pip_version}",
                f"{ALPINE_VERSION}-pip-{python3_pip_version}",
                f"pypy-{pypy_version}",
                f"{ALPINE_VERSION}-pypy-{pypy_version}",
                f"pypy-{pypy_version}-pip-{python3_pip_version}",
                f"{ALPINE_VERSION}-pypy-{pypy_version}-pip-{python3_pip_version}"
            ]
        }
    }

    remotes = [
        f"{REGISTRY}/{REPOSITORY_OWNER}"
    ]

    for name, content in iamges.items():
        print_banner(f"Processing: {name}")

        image = Image(
            name,
            content.get("path"),
            remotes=remotes
        )
        image.add_tag("latest")
        image.add_tag(ALPINE_VERSION)

        if content.get("args") is not None:
            for key, value in content.get("args").items():
                image.add_arg(key, value)

        if content.get("tags") is not None:
            for tag in content.get("tags"):
                image.add_tag(tag)

        print_tags(image.name, image.tags)

        print(
            Colours.Foreground.CYAN +
            "--- Build ---" +
            Colours.RESET,
            flush=True
        )
        image.build()
        print(
            Colours.Foreground.BLUE +
            "--- Push ---" +
            Colours.RESET,
            flush=True
        )
        image.push()


if __name__ == "__main__":
    main()

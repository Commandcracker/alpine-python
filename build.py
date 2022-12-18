
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
        system(f"{prefix}{self}{suffix}")

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

    ALPINE_VERSION = "3.17.0"

    pypy_version = "7.3.10"
    pypy2_7_sha256 = "55703da5a49021b7f0e134fc4ced26b26ca09ca95b66803f29a06aa06f3cf3fb"
    pypy3_8_sha256 = "349ca52c4a4f85ea0fbd82b74bf6b574f8c4105e51cb8915d5ed858fbda45491"
    pypy3_9_sha256 = "241f5a22cd2e5eb8a80d41f5c449e6c5978a144390e1e22679a35a30ce328f6c"

    python2_pip_version = "20.3.4"
    python2_pip_sha256 = "217ae5161a0e08c0fb873858806e3478c9775caffce5168b50ec885e358c199d"
    python2_pip_whl_name = "pip-20.3.4-py2.py3-none-any.whl"
    python2_pip_downlaod_url = "https://files.pythonhosted.org/packages/27/79/8a850fe3496446ff0d584327ae44e7500daf6764ca1a382d2d02789accf7/pip-20.3.4-py2.py3-none-any.whl"

    python3_pip_version = "22.3.1"
    python3_pip_sha256 = "908c78e6bc29b676ede1c4d57981d490cb892eb45cd8c214ab6298125119e077"
    python3_pip_whl_name = "pip-22.3.1-py3-none-any.whl"
    python3_pip_downlaod_url = "https://files.pythonhosted.org/packages/09/bd/2410905c76ee14c62baf69e3f4aa780226c1bbfc9485731ad018e35b0cb5/pip-22.3.1-py3-none-any.whl"

    pycparser_version = "2.21"
    pycparser_whl_name = "pycparser-2.21-py2.py3-none-any.whl"
    pycparser_sha256 = "8ee45429555515e1f6b185e78100aea234072576aa43ab53aefcae078162fca9"
    pycparser_downlaod_url = "https://files.pythonhosted.org/packages/62/d5/5f610ebe421e85889f2e55e33b7f9a6795bd982198517d912eb1c76e1a53/pycparser-2.21-py2.py3-none-any.whl"

    iamges = {
        # alpine-python2
        "alpine-python2": {
            "path": "images/python2",
            "args": {
                "ALPINE_VERSION": ALPINE_VERSION
            }
        },
        "alpine-python2-pip": {
            "path": "images/pip",
            "args": {
                "BASE_IMAGE": f"alpine-python2:{ALPINE_VERSION}",
                "PIP_WHL": python2_pip_whl_name,
                "PIP_SHA256": python2_pip_sha256,
                "PIP_URL": python2_pip_downlaod_url
            },
            "tags": [
                f"pip-{python2_pip_version}",
                f"{ALPINE_VERSION}-pip-{python2_pip_version}"
            ]
        },
        "alpine-python2-pycparser": {
            "path": "images/whl",
            "args": {
                "BASE_IMAGE": f"alpine-python2:{ALPINE_VERSION}",
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
        # pypy2
        "alpine-pypy2": {
            "path": "images/pypy",
            "args": {
                "BASE_IMAGE": f"alpine-python2-pycparser:{ALPINE_VERSION}",
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
        "alpine-pypy2-pip": {
            "path": "images/pip",
            "args": {
                "BASE_IMAGE": f"alpine-pypy2:{ALPINE_VERSION}",
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
        "alpine-pypy2-pycparser": {
            "path": "images/whl",
            "args": {
                "BASE_IMAGE": f"alpine-pypy2:{ALPINE_VERSION}",
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
                "BASE_IMAGE": f"alpine-pypy2-pycparser:{ALPINE_VERSION}",
                "PYTHON_VERSION": "3.8",
                "PYPY_VERSION": pypy_version,
                "PYPY_SHA256SUM": pypy3_8_sha256,
                "ALPINE_VERSION": ALPINE_VERSION
            },
            "tags": [
                f"pypy-{pypy_version}",
                f"{ALPINE_VERSION}-pypy-{pypy_version}"
            ]
        },
        "alpine-pypy3.8-pip": {
            "path": "images/pip",
            "args": {
                "BASE_IMAGE": f"alpine-pypy3.8:{ALPINE_VERSION}",
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
        # pypy3.9
        "alpine-pypy3.9": {
            "path": "images/pypy",
            "args": {
                "BASE_IMAGE": f"alpine-pypy2-pycparser:{ALPINE_VERSION}",
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
                "BASE_IMAGE": f"alpine-pypy3.9:{ALPINE_VERSION}",
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

import re
import setuptools

version = ""
requirements = ["aiohttp>=3.7.4,<4", "orjson", "websockets", "disnake>=2.12.0"]
with open("ytune/__init__.py") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        f.read(),
        re.MULTILINE,
    ).group(1)

if not version:
    raise RuntimeError("version is not set")

if version.endswith(("a", "b", "rc")):
    try:
        import subprocess

        p = subprocess.Popen(
            ["git", "rev-list", "--count", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, _ = p.communicate()
        if out:
            version += out.decode("utf-8").strip()
        p = subprocess.Popen(
            ["git", "rev-parse", "--short", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, _ = p.communicate()
        if out:
            version += "+g" + out.decode("utf-8").strip()
    except Exception:
        pass

with open("README.md") as f:
    readme = f.read()

setuptools.setup(
    name="ytune",
    author="Whymedream",
    version=version,
    url="https://github.com/Whymedream/ytune",
    packages=setuptools.find_packages(),
    license="MIT",
    description="YouTube-only Lavalink wrapper for disnake / YTuneBot",
    long_description=readme,
    package_data={"ytune": ["py.typed"]},
    include_package_data=True,
    install_requires=requirements,
    extras_require=None,
    classifiers=[
        "Framework :: AsyncIO",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet",
    ],
    python_requires=">=3.10",
    keywords=["ytune", "lavalink", "disnake", "youtube"],
)
#!/usr/bin/env python

import sys
from os import path

from setuptools import setup, find_packages


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

install_requires = ["aiohttp>=3.9"]

extras_require = {
    "docs": ["mkdocs-material", "mkdocstrings-python", "black"],
    "test": ["pytest>=8.3", "typeguard>=4.2"],
}

# Require python 3.12
if sys.version_info < (3, 12):
    sys.exit("'pulsefire' requires Python >= 3.12")

setup(
    name="pulsefire",
    version="2.0.24",
    author="Jian Huang",
    author_email="iann838dev@gmail.com",
    url="https://github.com/iann838/pulsefire",
    description="A modern and flexible Riot Games Python SDK.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=["Riot Games", "League of Legends", "Teamfight Tactics", "Valorant", "Legends of Runeterra", "API", "SDK", "asyncio"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.12",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Natural Language :: English",
    ],
    license="MIT",
    packages=find_packages(exclude=("tests", "transpile")),
    zip_safe=True,
    install_requires=install_requires,
    extras_require=extras_require,
    include_package_data=True,
)

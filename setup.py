import os
import subprocess

from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="stupid_dns_watchdog",
    version="0.0.1",
    description="Watchdog for changes in your external IP. Automatically pushes the changes to git.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Velythyl/stupid-dns-watchdog",
    author="Charlie Gauthier",
    author_email="charlie.gauthier@umontreal.ca",
    license="MIT",
    packages=find_packages(),
    install_requires=["python-crontab"],
    entry_points={
        "console_scripts": [
            "sdw=stupid_dns_watchdog.main:main",
        ]
    },
)
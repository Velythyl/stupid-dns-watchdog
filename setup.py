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
    name="litreview",
    version="0.0.1",
    description="Automate creation of Jekyll posts for literature reviews",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Velythyl/litreview",
    author="Charlie Gauthier",
    author_email="charlie.gauthier@umontreal.ca",
    license="MIT",
    packages=find_packages(exclude=("pdfs")),
    package_data={"litreview": ["*.yaml", "*.md"]},
    include_package_data=True,
    install_requires=["pyyaml", "beautifulsoup4", "validators", "six", "soupsieve", "twine"],
    entry_points={
        "console_scripts": [
            "litreview=litreview.main:main",
        ]
    },
)
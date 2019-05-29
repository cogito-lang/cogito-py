"""A tiny python library that links against libcogito"""

import pathlib
from setuptools import setup

README = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
    name="cogito",
    version="0.2.1",
    py_modules=["cogito"],
    description="A tiny python library that links against libcogito",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/cogito-lang/cogito-py",
    author="Kevin Deisz",
    author_email="kevin.deisz@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ]
)

#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="loansathi",
    version="0.1.0",
    author="Javed Gadiwala",
    description="Local loan eligibility and credit analysis tool for Chartered Accountants",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JavedGadiwala/loansathi",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.12",
    install_requires=requirements,
)

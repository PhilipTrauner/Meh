# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, "rst")
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, "r").read()

setup(
	name="Meh",
	version="1.0",
	author="Philip Trauner",
	author_email="philip.trauner@aol.com",
	url="https://github.com/PhilipTrauner/Meh",
	packages=find_packages(),
	test_suite="Tests.tests.tests",
	description="Python configuration files in Python.",
	long_description=read_md("README.md"),
	classifiers=[
		"Development Status :: 4 - Beta",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3.4",
		"Programming Language :: Python :: 3.5",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
	],
	keywords="config cfg meh py json"
)

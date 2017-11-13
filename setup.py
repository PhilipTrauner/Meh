# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

long_description = """Meh
===

.. figure:: http://content.philip-trauner.me/meh.png
   :alt: Meh Banner


|Python version support: 2.7, 3.4, 3.5| |License: MIT|

***Meh*** is a **Python configuration utility** that uses **Python** as
it’s **data format**. It provides a pleasant and very “pythonic”
interface to do all the things a configuration utility does, like
default values, validators and comments.


.. |Python version support: 2.7, 3.4, 3.5| image:: https://img.shields.io/badge/python-2.7%2C%203.4%2C%203.5-blue.svg
.. |License: MIT| image:: https://img.shields.io/badge/license-MIT-blue.svg
"""

setup(
	name="Meh",
	version="1.2.1",
	author="Philip Trauner",
	author_email="philip.trauner@arztpraxis.io",
	url="https://github.com/PhilipTrauner/Meh",
	packages=find_packages(),
	test_suite="tests.tests.tests",
	description="Python configuration files in Python.",
	long_description=long_description,
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3.4",
		"Programming Language :: Python :: 3.5",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
	],
	keywords=["config", "cfg", "meh", "py"]
)

#!/usr/bin/env python

from setuptools import setup


with open("README.rst") as fp:
    readme = fp.read()

setup(
    setup_requires=['pbr'],
    pbr=True
)

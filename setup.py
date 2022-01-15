#!/usr/bin/env python

import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="medium-apis",
    version="0.1.1",
    url="https://github.com/weeping-angel/medium-apis",
    license='MIT',

    author="Nishu Jain",
    author_email="nishujain1997.19@gmail.com",

    description="Python Wrapper on top of Medium API to quickly extract data from Medium's website (https://medium.com).",
    long_description=read("./docs/README.rst"),

    packages=find_packages(include=['medium_apis', 'medium_apis.*']),

    install_requires=['ujson'],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)

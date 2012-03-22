#!/usr/bin/env python

from setuptools import setup

setup(
    name='fzhidao',
    version='0.0.1',
    author='popomore',
    author_email='a@chuo.me',
    packages=['fzhidao'],
    license='BSD License',
    entry_points={
        'console_scripts': ['fzhidao= fzhidao.server:main'],
    },
    include_package_data=True,
    install_requires=['pyquery'],
)

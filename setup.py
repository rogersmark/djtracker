import os
from setuptools import setup, find_packages


setup(
    name = "djtracker",
    version = "0.2",
    author = "Mark Rogers",
    author_email = "f4nt@f4ntasmic.com",
    url = "http://www.f4ntasmic.com",

    packages = find_packages('.'),
    package_dir = {'':'.'},
    license = "BSD License",
    keywords = "django issue tracker",
    description = "An issue tracker built with django",
    install_requires=[
        '',
    ],
    classifiers = [
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        'Programming Language :: Python',
    ]
)


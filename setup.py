import os
from setuptools import setup, find_packages

setup(
    name = "djtracker",
    version = "0.3",
    author = "Mark Rogers",
    author_email = "f4nt@f4ntasmic.com",
    url = "http://www.f4ntasmic.com",

    packages = find_packages('.'),
    package_dir = {'':'.'},
    data_files=[('.', ['README.rst','MANIFEST.in', 'README']),],
    package_data = {
        'djtracker':
        ['templates/*.html',
         'templates/djtracker/*.html',
         'templates/registration/*',
         'fixtures/*.json',
        ],
    },
    include_package_data=True,

    license = "BSD License",
    keywords = "django issue tracker",
    description = "An issue tracker built with django",
    install_requires=[
        'gitpython',
        'django-registration',
    ],
    classifiers = [
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        'Programming Language :: Python',
    ]
)


import os
from setuptools import setup, find_packages

media_files = []

for dirpath, dirnames, filenames in os.walk('src/django_yaba/media'):
        media_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

setup(
    name = "djtracker",
    version = "0.2.1",
    author = "Mark Rogers",
    author_email = "f4nt@f4ntasmic.com",
    url = "http://www.f4ntasmic.com",

    packages = find_packages('.'),
    package_dir = {'':'.'},
    data_files=media_files,
    package_data = {
        'djtracker':
        ['templates/*.html']
    },
    include_package_data=True,

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


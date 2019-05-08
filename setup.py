
"""Packaging settings."""


from codecs import open
from os.path import abspath, dirname, join

from setuptools import find_packages, setup

from translate import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name = 'translate',
    version = __version__,
    description = 'Convert transcript coordinates into genomic coordinates',
    long_description = long_description,
    author = 'Seth Stadick',
    author_email = 'sstadick@gmail.com',
    license = 'UNLICENSE',
    classifiers = [
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords = ['translate', 'transcript'],
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires = ['click', 'dataclasses'],
    entry_points = {
        'console_scripts': [
            'translate=translate.cli:main',
        ],
    }
)
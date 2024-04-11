import os
import re
from codecs import open

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def read_version():
    regexp = re.compile(r'^VERSION\W*=\W*\(([^\(\)]*)\)')
    init_py = os.path.join(here, '__init__.py')
    with open(init_py, encoding='utf-8') as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1).replace(', ', '.')
        else:
            raise RuntimeError(
                'Cannot find version in __init__.py'
            )


github_url = 'https://github.com/bieli/IoText-data-protocol'

setup(
    name='IoText-data-protocol',
    version=read_version(),

    description='IoText data protocol Python library (spec. + serDe + builder)',
    long_description=long_description,

    url=github_url,

    author='Marcin Bielak',
    author_email='marcin.bieli+IoText+data+protocol@gmail.com',

    license='Apache',

    classifiers=[
        'Development Status :: 4 - Beta',


        'Environment :: Console',


        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',


        'License :: OSI Approved :: Apache License',


        'Operating System :: OS Independent',


        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',

        'Topic :: Database',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Information Analysis'
    ],

    keywords='Internet Of Things IoT IIoT data protocol',

    project_urls={
        'Documentation': 'https://github.com/bieli/IoText-data-protocol',
        'Changes': github_url + '/releases'
    },
    packages=find_packages('.', exclude=["tests*"]),
    python_requires='>=3.7, <4',
    install_requires=[],
    test_suite='pytest'
)

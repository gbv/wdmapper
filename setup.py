# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import re

version = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]+)[\'"]',
    open('wdmapper/version.py').read()
).group(1)

setup(
    name='wdmapper',
    version=version,
    description='Wikidata authority file mapping tool',
    author='Jakob Voß',
    author_email='jakob.voss@gbv.de',
    license='MIT',
    url='http://github.com/gbv/wdmapper',
    packages=find_packages(),
    install_requires=['pywikibot'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-pep8', 'pytest-cov'],
    download_url = 'https://github.com/gbv/wdmapper/tarball/' + version,
    keywords = ['wikidata', 'beacon', 'identifier'],
    entry_points={
        'console_scripts': [
            'wdmapper=wdmapper.cli:main'
        ]
    }
)

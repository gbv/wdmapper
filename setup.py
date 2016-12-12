# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import re

__version__ = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]+)[\'"]',
    open('wdmapper/wdmapper.py').read()
).group(1)

setup(
    name='wdmapper',
    version=__version__,
    description='Wikidata authority file mapping tool',
    author='Jakob Voß',
    author_email='jakob.voss@gbv.de',
    license='MIT',
    url='http://github.com/gbv/wdmapper',
    packages=find_packages(),
    install_requires=['pywikibot'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-pep8', 'pytest-cov'],
    entry_points={
        'console_scripts': [
            'wdmapper=wdmapper:main'
        ]
    }
)

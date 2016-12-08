# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='wdmapper',
    version='0.0.0',
    description='Wikidata authority file mapping tool',
    author='Jakob Voß',
    author_email='jakob.voss@gbv.de',
    license='MIT',
    url='http://github.com/gbv/wdmapper',
    packages=['wdmapper'],
    install_requires=['pywikibot'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest','pytest-cov'],
    entry_points={
        'console_scripts': [
            'wdmapper=wdmapper.wdmapper:main'
        ]
    }
)

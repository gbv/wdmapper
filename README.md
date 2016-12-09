# wdmapper

[![Build Status](https://travis-ci.org/gbv/wdmapper.png?branch=master)](https://travis-ci.org/gbv/wdmapper)
[![Coverage Status](https://coveralls.io/repos/github/gbv/wdmapper/badge.svg?branch=master)](https://coveralls.io/github/gbv/wdmapper?branch=master)
[![Requires.io](https://requires.io/github/gbv/wdmapper/requirements.svg?branch=master)](https://requires.io/github/gbv/wdmapper/requirements?branch=master)

Wikidata authority file mapping tool

## Description

This tool is a command line application to manage mappings between authority files in Wikidata. The current draft of wdmapper is limited to simple 1-to-1 mapping that only exist for concepts obvious unique identity such as people.

## Installation

wdmapper has not been released yet, so you need to directly clone the git repository:

~~~shell
$ git clone https://github.com/gbv/wdmapper.git
$ cd wdmapper
$ python setup.py install         # either global as root
$ python setup.py install --user  # or local at ~/.local/
~~~

Minimum requirement: Python 2.7

## Usage

Run `wdmapper -h` for basic help.

File `user-config.py` as required by pywikibot is created if needed.

By default the script reads comma separated values from STDIN.

## License

The source code is available at <https://github.com/gbv/wdmapper> and licensed
under the terms of the MIT license.

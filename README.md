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

Run `wdmapper help` or `wdmapper` without arguments for basic help. The calling
syntax is

~~~shell
wdmapper [command] [source] [target]
~~~

with `info` as default command. Source and target are Wikidata property given by
any of

* property id (e.g. "P214")
* property URI/URL (e.g. "<http://www.wikidata.org/entity/P214>" 
  or "<https://www.wikidata.org/wiki/Property:P214>")
* exact English property label (e.g. "VIAF ID")

Depending on command the script reads input mappings from a file or standard
input, and mappings from Wikidata.  Arguments source and target are required
for CSV input format but not in BEACON input format (*the latter not
implemented yet*).

File `user-config.py` (required by pywikibot) is created automatically, if
needed.

### Commands

#### info

Show information about given Wikidata properties. Try `wdmapper P214` for an example.

#### get

Get mappings from Wikidata.

*not implemented yet*

#### echo

Read input mappings.

#### check

Check whether all input mappings are also in Wikidata.

*not implemented yet*

#### diff

Compare input mappings and mappings at Wikidata.

*not implemented yet*

#### add

Add input mappings to mappings at Wikidata unless already there.

*not implemented yet*

#### sync

Align Wikidata mappings and input mappings by adding and removing mappings
in Wikidata: missing mappings are created and additional mappings are removed.
 
*not implemented yet*

## License

The source code is available at <https://github.com/gbv/wdmapper> and licensed
under the terms of the MIT license.

## See also

* BEACON
* pywikibot
* ...


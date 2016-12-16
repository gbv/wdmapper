# wdmapper

[![Build Status](https://travis-ci.org/gbv/wdmapper.png?branch=master)](https://travis-ci.org/gbv/wdmapper)
[![Coverage Status](https://coveralls.io/repos/github/gbv/wdmapper/badge.svg?branch=master)](https://coveralls.io/github/gbv/wdmapper?branch=master)
[![Requires.io](https://requires.io/github/gbv/wdmapper/requirements.svg?branch=master)](https://requires.io/github/gbv/wdmapper/requirements?branch=master)

Wikidata authority file mapping tool

## Description

This tool is a command line application to manage mappings between authority files in Wikidata. The current draft of wdmapper is limited to simple 1-to-1 mapping that only exist for concepts obvious unique identity such as people.

## Installation

Install releases via pip

~~~shell
$ pip install wdmapper          # install global as root
$ pip install wdmapper --user   # or local at ~/.local
~~~

To get latest developer version directly clone the git repository:

~~~shell
$ git clone https://github.com/gbv/wdmapper.git
$ cd wdmapper
$ git checkout dev                # optionally checkout some branch
$ python setup.py install         # either
$ python setup.py install --user  # or
~~~

Minimum requirement: Python 2.7

## Usage

Run `wdmapper help` or `wdmapper` without arguments for basic help. The calling
syntax is

~~~shell
wdmapper [command] [source] [target]
~~~

with `property` as default command. Source and target are Wikidata property
given by any of

* property id (e.g. "P214")
* property URI/URL (e.g. "<http://www.wikidata.org/entity/P214>" 
  or "<https://www.wikidata.org/wiki/Property:P214>")
* exact English property label (e.g. "VIAF ID")

Depending on command the script reads input mappings from a file or standard
input, and mappings from Wikidata.  Arguments source and target are required
for CSV input format but not in BEACON input format.

File `user-config.py` (required by pywikibot) is created automatically, if
needed.

### Commands

#### property

Show information about given Wikidata properties. Examples:

~~~shell
$ wdmapper P214
$ wdmapper "VIAF ID"
$ wdmapper https://viaf.org/viaf/
~~~

#### get

Get mappings from Wikidata. Default output format is BEACON. Examples:

~~~shell
$ wdmapper get P214 --limit 10
$ wdmapper get P214 P2428 --limit 10
~~~

See [Wikidata BEACON generator] for an online tool to get the same data.

#### echo

Read input mappings to check or translate between formats. 

*Not fully implemented yet.*

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

* BEACON format specification
* [Wikidata BEACON generator]
* pywikibot
* ...

[Wikidata BEACON generator]: https://tools.wmflabs.org/wikidata-todo/beacon.php

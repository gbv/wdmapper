wdmapper
========

.. image:: https://badge.fury.io/py/wdmapper.svg
    :target: https://badge.fury.io/py/wdmapper

.. image:: https://travis-ci.org/gbv/wdmapper.png?branch=master
    :target: http://travis-ci.org/gbv/wdmapper

.. image:: https://coveralls.io/repos/gbv/wdmapper/badge.svg?branch=master 
    :target: https://coveralls.io/r/gbv/wdmapper?branch=master 

.. image:: https://requires.io/github/gbv/wdmapper/requirements.svg?branch=master
    :target: https://requires.io/github/gbv/wdmapper/requirements?branch=master

Wikidata authority file mapping tool

Description
-----------

This tool is a command line application to manage mappings between
authority files in Wikidata. The current draft of wdmapper is limited to
simple 1-to-1 mapping that only exist for concepts obvious unique
identity such as people.

Requirements
------------

Python 2.7 or higher


Installation
------------

.. code:: shell

    $ pip install wdmapper

Usage
-----

Run ``wdmapper help``, ``wdmapper -h`` or ``wdmapper --help`` for basic help.
The general calling syntax is

.. code:: shell

    wdmapper [command] [source] [target]

with ``property`` as default command. Source and target are Wikidata
property given by any of

-  property id (e.g. "P214")
-  property URI/URL (e.g. "http://www.wikidata.org/entity/P214" or
   "https://www.wikidata.org/wiki/Property:P214")
-  exact English property label (e.g. "VIAF ID")

Depending on command the script reads input mappings from a file or
standard input, and mappings from Wikidata. Arguments source and target
are required for CSV input format but not in BEACON input format.

File ``user-config.py`` (required by pywikibot) is created
automatically, if needed.

Commands
~~~~~~~~

property
^^^^^^^^

Show information about given Wikidata properties. Examples:

.. code:: shell

    $ wdmapper P214
    $ wdmapper "VIAF ID"
    $ wdmapper https://viaf.org/viaf/

get
^^^

Get mappings from Wikidata. Default output format is BEACON. Examples:

.. code:: shell

    $ wdmapper get P214 --limit 10
    $ wdmapper get P214 P2428 --limit 10

See `Wikidata BEACON
generator <https://tools.wmflabs.org/wikidata-todo/beacon.php>`__ for an
online tool to get the same data.

convert
^^^^^^^

Read input mappings to check or translate between formats.

*Not fully implemented yet.*

check
^^^^^

Check whether all input mappings are also in Wikidata.

*not implemented yet*

diff
^^^^

Compare input mappings and mappings at Wikidata. This can be used for
instance to regularly check whether mappings at Wikidata have been
changed:

.. code:: shell

    $ wdmapper get P214 P2428 > mappings.csv
    $ # ...wait until Wikidata could have been modified...
    $ wdmapper diff P214 P2428 < mappings.csv

add
^^^

Add input mappings to mappings at Wikidata unless already there.

*not implemented yet*

sync
^^^^

Align Wikidata mappings and input mappings by adding and removing
mappings in Wikidata: missing mappings are created and additional
mappings are removed.

*not implemented yet*

License
-------

The source code is available at https://github.com/gbv/wdmapper and
licensed under the terms of the MIT license.

See also
--------

-  BEACON format specification
-  `Wikidata BEACON
   generator <https://tools.wmflabs.org/wikidata-todo/beacon.php>`__
-  pywikibot
-  ...


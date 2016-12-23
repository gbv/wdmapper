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

See <https://wdmapper.readthedocs.io/> for full documentation.

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


License
-------

The source code is available at https://github.com/gbv/wdmapper and
licensed under the terms of the MIT license.

See also
--------

-  BEACON format specification
-  `Wikidata BEACON
   generator <https://tools.wmflabs.org/wikidata-todo/beacon.php>`__
-  https://www.wikidata.org/wiki/User:ZbwAddAuthorityBot
-  pywikibot
-  ...


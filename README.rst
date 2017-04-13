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

See https://wdmapper.readthedocs.io/ or source folder ``docs`` for full
documentation.

Description
~~~~~~~~~~~

**wdmapper** is a command line application and Python library to manage
mappings between authority files in Wikidata. The current draft is limited to
simple 1-to-1 mapping that only exist for concepts of obviously unique identity
such as people.

Installation
~~~~~~~~~~~~

.. code:: shell

    $ pip install wdmapper

Usage
~~~~~

The general calling syntax is

.. code:: shell

    wdmapper [OPTIONS] COMMAND [SOURCE] TARGET

where ``COMMAND`` is a wdmapper command, ``TARGET`` is a Wikidata property, and
``SOURCE`` is an optional Wikidata property for indirect links. ``TARGET`` can
also be omitted when read from a BEACON file. Depending on the command wdmapper
reads input mappings from a file or standard input and/or Wikidata and writes
them to standard output or a file.

Run ``wdmapper`` without command line arguments (or with option ``--help|-h``)
for a list of command line input, and mappings from Wikidata.  options. 


License
~~~~~~~

The source code is available at https://github.com/gbv/wdmapper and
licensed under the terms of the MIT license.

See also
~~~~~~~~

-  BEACON format specification
-  `Wikidata BEACON
   generator <https://tools.wmflabs.org/wikidata-todo/beacon.php>`__
-  https://www.wikidata.org/wiki/User:ZbwAddAuthorityBot
-  pywikibot
-  ...


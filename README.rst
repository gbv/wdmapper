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
simple 1-to-1 mapping that only exist for concepts obvious unique identity such
as people.

Installation
~~~~~~~~~~~~

.. code:: shell

    $ pip install wdmapper

Usage
~~~~~

Run ``wdmapper help``, ``wdmapper -h`` or ``wdmapper --help`` for basic help.
The general calling syntax is

.. code:: shell

    wdmapper [OPTIONS] COMMAND [SOURCE] TARGET

where ``COMMAND`` is one of the wdmapper commands and ``SOURCE`` and ``TARGET``
are Wikidata properties. 

Depending on the command the script reads input mappings from a file or
standard input, and mappings from Wikidata. Arguments SOURCE and TARGET are
required for CSV input format but not for BEACON input format.

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


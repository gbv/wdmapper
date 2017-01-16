Commands
========

wdmapper provides several commands to perform different tasks.


get
---

Get mappings from Wikidata based on given :doc:`properties <properties>`.
Examples:

.. code:: shell

    $ wdmapper get P214 --limit 10
    $ wdmapper get P214 P2428 --limit 10

Output format can be controlled with option ``to`` having BEACON format as
default.  Number and order of results can be influenced by options ``limit``
and ``sort``.  See `Wikidata BEACON generator
<https://tools.wmflabs.org/wikidata-todo/beacon.php>`__ for a similar online
tool.


head
-----

Get information about given properties. This command works similar to command
`get` but no mappings are retrieved. This is the default command if properties
are specified as additional command line arguments. Examples:

.. code:: shell

    $ wdmapper head P214
    $ wdmapper P214
    $ wdmapper "VIAF ID"
    $ wdmapper https://viaf.org/viaf/


check
-----

Check whether all input mappings are also in Wikidata.

.. code:: shell

    $ wdmapper get P214 P2428 --sort --limit 10 --to csv > mappings.csv
    $ # ...wait until Wikidata could have been modified...
    $ wdmapper check P214 P2428 < mappings.csv


Each output line is preceded by a marker to indicate which input mappings have
been found in Wikidata and how mappings in Wikidata differ from input mappings:

- If the same link was found in Wikidata, it is preceded by "="

- If a same link was found in Wikidata but with different annotation
  (different item or item label), it is preceded by "~"

- If the link was not found in Wikidata is is preceded by "+". Following link 
  lines starting with "-" indicate that other links would have to be removed
  or merged to add the missing link to Wikidata.

Use command `diff` instead to compare full sets of mappings.

Use cases:

* Detect mapping changes in Wikidata
* Check whether mappings can be added to Wikidata
* Lookup mappings for given identifiers

Example::

    echo ,114 | ./wdmapper.py --no-header check P757


diff
----

Compare input mappings and mappings at Wikidata. This can be used for
instance to regularly check whether mappings at Wikidata have been
changed:

.. code:: shell

    $ wdmapper get P214 P2428 -t csv > mappings.csv
    $ # ...wait until Wikidata could have been modified...
    $ wdmapper diff P214 P2428 -t csv < mappings.csv

Each output line is preceded by "+ " if an input link is missing in Wikidata or
"- " if a link from Wikidata is missing in the input.

The output is sorted by links. Option "limit" implies option "sort" to get
stable results. Use command `check` instead to compare a limited set of
mappings against mappings on Wikidata.


convert
-------

Read input mappings to check or translate between mapping formats.  This is the
default command if no properties have been specified as command line arguments.
Examples:

.. code:: shell

    $ wdmapper convert -i mappings.csv -t beacon
    $ wdmapper convert -f csv -t beacon < mappings.csv > mappings.txt


add
---

Add input mappings to mappings at Wikidata unless already there. Better first
try command `check` and/or command "add" with option "dry" to find out what
statements would be added to Wikidata.

*not implemented yet*


sync
----

Align Wikidata mappings and input mappings by adding and removing
mappings in Wikidata: missing mappings are created and additional
mappings are removed.

*not implemented yet*


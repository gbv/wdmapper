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

Each output line is preceded with "+ ", "- ", or "= " to indicate which links
differ or are equal.

Please use command diff instead if working on full sets of links.


diff
----

Compare input mappings and mappings at Wikidata. This can be used for
instance to regularly check whether mappings at Wikidata have been
changed:

.. code:: shell

    $ wdmapper get P214 P2428 -t csv > mappings.csv
    $ # ...wait until Wikidata could have been modified...
    $ wdmapper diff P214 P2428 -t csv < mappings.csv

Each output line is preceded with "+ " or "- " to indicate which links 
differ.


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

Add input mappings to mappings at Wikidata unless already there.

*not implemented yet*


sync
----

Align Wikidata mappings and input mappings by adding and removing
mappings in Wikidata: missing mappings are created and additional
mappings are removed.

*not implemented yet*


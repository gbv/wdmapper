Commands
========

wdmapper provides several commands to perform different tasks.

property
--------

Show information about given Wikidata properties. Examples:

.. code:: shell

    $ wdmapper P214
    $ wdmapper "VIAF ID"
    $ wdmapper https://viaf.org/viaf/

get
---

Get mappings from Wikidata. Default output format is BEACON. Examples:

.. code:: shell

    $ wdmapper get P214 --limit 10
    $ wdmapper get P214 P2428 --limit 10

See `Wikidata BEACON
generator <https://tools.wmflabs.org/wikidata-todo/beacon.php>`__ for an
online tool to get the same data.

convert
-------

Read input mappings to check or translate between formats.

.. code:: shell

    $ wdmapper convert -i mappings.csv -t beacon
    $ wdmapper convert -f csv -t beacon < mappings.csv > mappings.txt
 
diff
----

Compare input mappings and mappings at Wikidata. This can be used for
instance to regularly check whether mappings at Wikidata have been
changed:

.. code:: shell

    $ wdmapper get P214 P2428 > mappings.csv
    $ # ...wait until Wikidata could have been modified...
    $ wdmapper diff P214 P2428 < mappings.csv

check
-----

Check whether all input mappings are also in Wikidata.

*not implemented yet*

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


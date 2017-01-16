Options
=======

wdmapper can be controlled by several parameters. Run the command line client
with option ``--help`` to get a full list of command line arguments.

Input and output
----------------

Option **input** (``--input`` or ``-i``) and option **output** (``--output`` or
``-o``) can be used to select an input or output **file**. The special value
``-`` is used as default to denote the standard input or standard output,
respectively. Input is always assumed to be Unicode in UTF-8 encoding.

Option **from** (``--from`` or ``-f``) and option **to** (``--to`` or ``-t``)
can be used to select input or output **format**. Default input format is
``csv`` and default output format is ``beacon``. If no input/output format has
been specified, it is guessed from input/output filename extension, for
instance ``.csv`` for CSV format and ``.txt`` for BEACON format.

Supported formats
^^^^^^^^^^^^^^^^^

input formats: csv

output formats: csv, beacon, nt

Examples
^^^^^^^^

.. code:: shell

    $ wdmapper convert -i mappings.csv -o mappings.txt
    $ wdmapper convert < mappings.csv -t beacon > mappings.txt


Mapping retrieval
-----------------

limit
^^^^^

Limit maximum number of mappings to process.

sort
^^^^

Sort mappings (alphabetically) for stable output. This can slow down the query
so only use if needed. set to ``False`` by default.

language
^^^^^^^^

Specify language of labels. English ("en") is used by default.

type
^^^^

Filter Wikidata items to instances of some class or its subclasses. For
instance the value `Q5 <https://www.wikidata.org/wiki/Q5>`_ (human) will only
include mappings with Wikidata items about humans. Keep in mind that not all
Wikidata items have proper instance statements and the class hierarchy often
contains errors and unexpected subclasses!  See `wdtaxonomy
<https://www.npmjs.com/package/wikidata-taxonomy>`_ for another command line
tool to examine the Wikidata class hierarchy.

This option is ignored for command "check"!

cache
^^^^^

Disable caching. Set to ``False`` by default.

sparql
^^^^^^

Wikidata SPARQL endpoint, set to ``http://query.wikidata.org/sparql`` by
default.

Wikidata editing
----------------

*Changing Wikidata has not been implemented yet.*

dry
^^^

Don't perform any edits on Wikidata


Additional output control
-------------------------

header
^^^^^^

Read/write CSV/BEACON without header. *This option is experimental.*

relation
^^^^^^^^

Mapping relation URI such as ``skos:exactMatch`` or ``owl:sameAs``.

debug
^^^^^

Enable debugging mode.


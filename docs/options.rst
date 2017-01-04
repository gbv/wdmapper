Options
=======

wdmapper can be controlled by several parameters. Run the command line client
with option ``--help`` to get a full list of command line arguments.

Input and output
----------------

Option ``input`` (``--input`` or ``-i``) and option ``output`` (``--output`` or
``-o``) can be used to select an **input or output file**. The special value
``-`` is used as default to denote the standard input or standard output,
respectively. Input is always assumed to be Unicode in UTF-8 encoding.

Option ``from`` (``--from`` or ``-f``) and option ``to`` (``--to`` or ``-t``)
can be used to select **input or output format**. Default input format is
``csv`` and default output format is ``beacon``. If no input/output format has
been specified, it is guessed from input/output filename extension, for
instance ``.csv`` for CSV format and ``.txt`` for BEACON format.

Supported input formats are: csv

Supported output formats are: csv, beacon, nt

Examples
^^^^^^^^

.. code:: shell

    $ wdmapper convert -i mappings.csv -o mappings.txt
    $ wdmapper convert < mappings.csv -t beacon > mappings.txt

Additional options and arguments
--------------------------------

``limit``, ``sort``, ``debug``, ``cache``, ``header``, ``dry``, ``relation``


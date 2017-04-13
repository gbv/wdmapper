Command Line
============

wdmapper comes with a command line client of same name.  The general calling
syntax is

.. code:: shell

    $ wdmapper [OPTIONS] COMMAND TARGET          # for direct links
    $ wdmapper [OPTIONS] COMMAND SOURCE TARGET   # for indirect links

where ``COMMAND`` is one of the wdmapper :doc:`commands <commands>` and
``SOURCE`` and ``TARGET`` are Wikidata :doc:`properties <properties>`.  A list
of commands and :doc:`options <options>` is shown with option ``-h`` or
``--help``:

.. code:: shell

    $ wdmapper --help


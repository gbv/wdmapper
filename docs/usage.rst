Usage
=====

wdmapper can be used both, as :doc:`command line application <cli>` and as
:doc:`Python library <api>`. This document focuses on the command line client
but its functionality can also used in pure Python code.

Get mappings and property information
-------------------------------------

The following call looks up three :doc:`mappings <mappings>` from Wikidata to
`World Heritage Site identifiers <http://whc.unesco.org/en/list/>`_ as assigned
by UNESCO::

    $ wdmapper get P757 --limit 3

Wikidata :doc:`properties <properties>` can also be referenced by label, URI or
URL. The call could also be written like this::

    $ wdmapper get 'World Heritage Site ID' --limit 3
    $ wdmapper get 'http://whc.unesco.org/en/list/' --limit 3
    $ wdmapper get 'https://www.wikidata.org/wiki/Property:P757' --limit 3

To get the mappings in stable order, add option :ref:`sort`.  The default
output format BEACON includes mapping metadata before the actual mappings::

    $ wdmapper get P757 --limit 3 --sort
    #FORMAT: BEACON
    #NAME: World Heritage Site ID
    #DESCRIPTION: Mapping from Wikidata IDs to World Heritage Site IDs
    #PREFIX: http://www.wikidata.org/entity/
    #TARGET: http://whc.unesco.org/en/list/

    Q319841|Luxor Temple|087-002
    Q38095|Galápagos Islands|1
    Q6153869|Lower Valley of the Awash|10

Command :ref:`head` only emits metadata, for instance to quickly look up a
Wikidata property.  This command is assumed as default if additional arguments
are given so the following calls are equivalent::

    $ wdmapper head P757
    $ wdmapper P757

Output formats such as CSV emit mappings without metadata::

    $ wdmapper get P757 --limit 3 --sort --to csv
    source, target, annotation
    Q319841, 087-002, Luxor Temple
    Q38095, 1, Galápagos Islands
    Q6153869, 10, Lower Valley of the Awash

The second output line tells that Wikidata item with id ``Q319841`` (source
column) is linked to World Heritage Site with id ``087-002`` (target column).
The third column (annotation, put in the middle in BEACON format) gives the
item label for better readability.

In NTriples output format, identifiers are expanded to full URIs. The expansion
is based on URI templates of each property (see metadata fields PREFIX and
TARGET above)::

    $ wdmapper get P757 --limit 3 --sort --to nt --relation owl:sameAs
    <http://www.wikidata.org/entity/Q319841> <http://www.w3.org/2002/07/owl#sameAs> <http://whc.unesco.org/en/list/087-002> .
    <http://www.wikidata.org/entity/Q38095> <http://www.w3.org/2002/07/owl#sameAs> <http://whc.unesco.org/en/list/1> .
    <http://www.wikidata.org/entity/Q6153869> <http://www.w3.org/2002/07/owl#sameAs> <http://whc.unesco.org/en/list/10> .

The last example shows how to connect multiple authority files. If two
properties are given, wdmapper retrieves mappings from the first (source) to
the second (target). The following call lists all Wikidata items that have both
a `TED speaker ID <http://www.wikidata.org/entity/P2611>`_, and a `Find a Grave
grave ID <http://www.wikidata.org/entity/P535>`_)::

    $ wdmapper get P2611 P535
    #FORMAT: BEACON
    #NAME: Find a Grave grave ID
    #DESCRIPTION: Mapping from TED speaker IDs to Find a Grave grave IDs
    #PREFIX: https://www.ted.com/speakers/
    #TARGET: http://www.findagrave.com/cgi-bin/fg.cgi?page=gr&GRid=

    viktor_e_frankl|Q154723|14540087
    jimmy_carter|Q23685|6734
    john_wooden|Q551032|53261713
    douglas_adams|Q42|22814
    roger_ebert|Q212173|107806860
    denis_dutton|Q1187362|63438326

In the case of such "indirect links", the annotation field is used to give the
Wikidata item identifier.

Check mappings and identifiers
------------------------------

Command :ref:`check` and command :ref:`diff` both compare mappings and/or
identifiers provided from input file and mappings in Wikidata.

For instance check whether Q42 still has the Find a Grave ID 22814::

    $ echo Q42,22814 | wdmapper --no-header check P535
    ~ Q42|Douglas Adams|22814


Properties
==========

Each `Wikidata property <https://www.wikidata.org/wiki/Help:Properties>`__ has
a unique identifier build of "P" followed by a natural number. For instance
"P40" denotes the property "child" that is used to connect Wikidata items about
parents with items about their childs.  wdmapper requires properties to have an
URL template and to be of datatype external identifier: this applies for
instance to "P214" but not to "P40".

Properties in wdmapper can be referred to in different ways. The following
examples execute the :doc:`command line client <cli>` with default command
``head``:

- by property identifier

    .. code:: shell

        $ wdmapper P214

- by Wikidata property URI or URL

    .. code:: shell

        $ wdmapper http://www.wikidata.org/entity/P214
        $ wdmapper https://www.wikidata.org/wiki/Property:P214

- by property `URL template <https://www.wikidata.org/wiki/Property:P1630>`__.
  The placeholder ``$1`` can be omitted at the end of the URL.

    .. code:: shell

        $ wdmapper 'https://viaf.org/viaf/$1'
        $ wdmapper https://viaf.org/viaf/

- by property label

    .. code:: shell

        $ wdmapper 'VIAF ID'

Target and source property can also be specified in input format BEACON.

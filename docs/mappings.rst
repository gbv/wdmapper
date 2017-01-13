Mappings
========

*This introduction needs to be expanded to better explain authority files!*

wdmapper is a tool to manage mappings between authority files. What does this
mean?

The current version of wdmapper is limited to simple 1-to-1 mappings, also
referred to as **Links**. Two kinds of links are supported:

- direct links from Wikidata items to external identifiers that is
  given by a target :doc:`property <properties>`

- indirect links from an external source identifier, given by a source
  :doc:`property <properties>`, to external target identifier, given by a
  target :doc:`property <properties>`, The link is possible through a common
  Wikidata item that uses both source property and target property.

Each link consists of

- a source URI, specified in abbreviated form as source ID
- a target URI, specified in abbreviated form as target ID

The type of link ("relation") can optionally be configured with :doc:`option
<options>` ``relation``.

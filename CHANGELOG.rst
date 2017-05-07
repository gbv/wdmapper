History
=======

0.0.13 (2017-04-19)
-------------------
-  Use empty string instead of Wikidata-ID as default annotation
-  Allow to disable labels by setting language to empty string 

0.0.13 (2017-04-19)
-------------------
-  Extend output formats
-  Fix Unicode output when writing to files

0.0.9 (2017-04-13)
------------------
-  Add 'quicks' output format for deltas to be used in QuickStatements tool
-  Remove 'help' command

0.0.8 (2017-04-06)
------------------
-  Add 'json' output format (JSKOS Concept Mappings, .ndjson)
-  Include source and target concept scheme URI if available

0.0.7 (2017-01-17)
------------------
-  Add option 'language' to select language of labels
-  Add option 'sparql' to customize Wikidata SPARQL endpoint
-  Add option 'type' to filter Wikidata items by class

0.0.6 (2017-01-13)
------------------
-  Add basic support of BEACON input format
-  Improve lookup of properties by label

0.0.5 (2017-01-05)
------------------
-  Add ntriples output format
-  Add option 'relation'
-  Fix command 'check' for indirect links
-  Fix lookup of properties by URL template

0.0.4 (2017-01-03)
------------------
-  Implement command 'check'
-  Rename command 'about' to 'head'
-  Include item label for one-way mappings from Wikidata

0.0.3 (2016-12-23)
--------------------
-  Rename command 'echo' to 'convert'
-  Use command 'convert' by default
-  Fix and extend input/output from stdin/stdout and files

0.0.2 (2016-12-20)
------------------
-  Add BEACON output format
-  Implement command 'diff'
-  Add arguments --sort and --no-cache

0.0.1 (2016-12-16)
------------------
-  First release at PyPI
-  Implemented lookup of properties and mappings (commands 'property' and 'get')

0.0.0 (2016-12-08)
------------------
-  Create repository boilerplate

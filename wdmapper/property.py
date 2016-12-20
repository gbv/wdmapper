# -*- coding: utf-8 -*-
"""Get and express information about a Wikidata property."""

from __future__ import unicode_literals
import json
import re

from .exceptions import WdmapperError
from .sparql import sparql_query


class Property(object):
    """Representation of a Wikidata property"""

    id_pattern = re.compile(r"""
        ^
        (http://www.wikidata.org/entity/
        |https?://www.wikidata.org/wiki/Property:)?
        [Pp]
        (?P<id>[0-9]+)
        $""", re.VERBOSE)

    ns_pattern = re.compile('^[a-z]+:[^<>]+')

    def __init__(self, data):
        self.uri = data.get('p')
        if (self.uri):
            self.id = Property.match(self.uri)
        self.label = data.get('label')
        self.regex = data.get('regex')
        self.pattern = data.get('pattern')
        if (self.pattern):
            pattern = self.pattern.replace('$1','{ID}')
            self.beacon_pattern = re.sub(r'{ID}$','', pattern)

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        s = "{label} ({id})\n<{uri}>\n".format(**self.__dict__)
        if self.pattern:
            s += self.pattern
        s += "\n"
        if self.regex:
            s += self.regex
        return s

    @staticmethod
    def match(s):
        m = Property.id_pattern.match(s)
        if m:
            return 'P' + m.group('id')

    @classmethod
    def lookup(cls, s, cache=True):
        """check and normalize property value such as 'P32'"""

        pid = Property.match(s)
        if pid:
            # get by property id
            uri = 'http://www.wikidata.org/entity/' + pid
            where = 'BIND(<' + uri + '> AS ?p)'
        elif Property.ns_pattern.match(s):
            # get by formatting URL (P1630)
            formatter_url = json.dumps(s)   # quote and escape literal
            if formatter_url.find('$1') == -1:
                formatter_url += '$1'
            where = '?p wdt:P1630 %s' % formatter_url
        else:
            # get by label
            label = json.dumps(s)           # quote and escape literal
            where = '?p rdfs:label ?l . FILTER (str(?l) = %s)' % label

        query = """\
                SELECT ?p ?label ?pattern ?regex WHERE {{
                    {0} .
                    ?p a wikibase:Property .
                    OPTIONAL {{ ?p wdt:P1630 ?pattern }}
                    OPTIONAL {{ ?p wdt:P1793 ?regex }}
                    SERVICE wikibase:label {{
                        bd:serviceParam wikibase:language "{1}" .
                        ?p rdfs:label ?label .
                    }}
                }}""".format(where, 'en')

        res = sparql_query(query, cache=cache)

        if not res:
            raise WdmapperError("property not found: " + s)
        if len(res) > 1:
            raise WdmapperError("multiple properties: " + s)

        return cls(res[0])

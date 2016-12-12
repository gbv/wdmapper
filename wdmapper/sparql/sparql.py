# -*- coding: utf-8 -*-
"""SPARQL Query interface to Wikidata."""

import json
import sys
if sys.version_info[0] > 2:
    from urllib.parse import quote
    from urllib.request import Request, urlopen
else:
    from urllib2 import quote, Request, urlopen

WIKIDATA = 'http://query.wikidata.org/sparql'


def sparql_query(query, endpoint=WIKIDATA):
    url = '%s?query=%s' % (endpoint, quote(query))
    req = Request(url)
    req.add_header('cache-control', 'no-cache')
    req.add_header('Accept', 'application/sparql-results+json')

    res = urlopen(req).read()
    if res:
        data = json.loads(res)
    if data and 'results' in data:
        result = []
        qvars = data['head']['vars']
        for row in data['results']['bindings']:
            values = {}
            for var in qvars:
                if var in row:
                    values[var] = row[var]['value']
                else:
                    values[var] = None
            result.append(values)
    return result

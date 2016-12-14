# -*- coding: utf-8 -*-
"""SPARQL Query interface to Wikidata."""

from __future__ import unicode_literals
import json
import sys

PYTHON3 = sys.version_info[0] > 2

if PYTHON3:
    from urllib.parse import quote
    from urllib.request import Request, urlopen
else:
    from urllib2 import quote, Request, urlopen

WIKIDATA = 'http://query.wikidata.org/sparql'


def sparql_query(query, endpoint=WIKIDATA, cache=True):
    url = '%s?query=%s' % (endpoint, quote(query))
    req = Request(url)
    if not cache:
        req.add_header('cache-control', 'no-cache')
    req.add_header('Accept', 'application/sparql-results+json')

    res = urlopen(req).read()
    if PYTHON3:
        res = res.decode('utf8')

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

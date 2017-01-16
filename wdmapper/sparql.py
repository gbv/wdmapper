# -*- coding: utf-8 -*-
"""SPARQL Query interface to Wikidata."""

from __future__ import unicode_literals
import json
import sys
import textwrap

from .exceptions import WdmapperError

PY3 = sys.version_info[0] > 2

if PY3:
    from urllib.parse import quote
    from urllib.request import Request, HTTPError, URLError, urlopen
else:
    from urllib2 import quote, Request, HTTPError, URLError, urlopen

WIKIDATA = 'http://query.wikidata.org/sparql'


class SparqlEndpoint:

    def __init__(self, endpoint=WIKIDATA, cache=True, debug=False):
        self.endpoint = endpoint
        self.cache = cache
        self.debug = debug

    def query(self, query):
        query = textwrap.dedent(query)
        if self.debug:
            self.debug(query)

        url = '%s?query=%s' % (self.endpoint, quote(query))
        req = Request(url)
        if not self.cache:
            req.add_header('cache-control', 'no-cache')
        req.add_header('Accept', 'application/sparql-results+json')

        try:
            res = urlopen(req).read()
        except (URLError) as e:
            raise WdmapperError(e)

        if PY3:
            res = res.decode('utf8')

        if res:
            try:
                data = json.loads(res)
            except ValueError as e:
                raise WdmapperError(e)
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

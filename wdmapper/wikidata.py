# -*- coding: utf-8 -*-
"""Access Wikidata."""

from __future__ import unicode_literals
import json
import sys

from .exceptions import WdmapperError
from .sparql import SparqlEndpoint
from .property import Property
from .link import Link

from .queries import links_query, delta_query


def get_property(p, endpoint, language='en'):
    """Get property data from Wikidata."""

    if language is None:
        language = 'en'

    pid = Property.match(p)
    if pid:
        # get by property id
        uri = 'http://www.wikidata.org/entity/' + pid
        where = 'BIND(<' + uri + '> AS ?p)'
    elif Property.ns_pattern.match(p):
        # get by URL templateL (P1630)
        url = p + '$1' if p.find('$1') == -1 else p
        template = json.dumps(url)   # quote and escape literal
        where = '?p (wdt:P1921|wdt:P1630) %s' % (template)
    else:
        # get by label
        label = json.dumps(p)           # quote and escape literal
        where = '?p rdfs:label ?l . FILTER (str(?l) = %s)' % label

    query = """\
            SELECT DISTINCT ?p ?label ?template ?pattern ?type (SAMPLE(?kos) AS ?scheme) WHERE {{
                {0} .
                ?p a wikibase:Property .
                ?p wikibase:propertyType ?type .
                OPTIONAL {{ ?p wdt:P1921 ?template }}
                OPTIONAL {{ ?p wdt:P1630 ?template }}
                OPTIONAL {{ ?p wdt:P1793 ?pattern }}
                OPTIONAL {{
                  {{ ?p wdt:P1629 ?kos }}
                  UNION
                  {{ ?kos wdt:P1687 ?p }}
                }}
                SERVICE wikibase:label {{
                    bd:serviceParam wikibase:language "{1}" .
                    ?p rdfs:label ?label .
                }}
            }} GROUP BY ?p ?label ?template ?pattern ?type
    """.format(where, language)

    properties = []
    for row in endpoint.query(query):
        properties.append(Property(row))

    if not properties:
        raise WdmapperError('property not found: %s' % p)

    if len(properties) > 1:
        raise WdmapperError('multiple properties:\n' + '\n'.join(
                            [str(p) for p in properties]))

    return properties[0]


def get_links(source, target, endpoint, sort=False, limit=0, language='en', type='', **args):
    """Get an iterator of links with given properties."""

    query = links_query(source, target, sort, limit, language, type)

    res = endpoint.query(query)

    for row in res:
        yield _link_from_wdsparql_row(row)


def get_deltas(source, target, links, endpoint, language='en', **args):
    """Check a list of links against Wikipedia and return deltas.

    A delta is a list of changes, each a tuple of operator (character) and link.
    In contrast to diffs, the same change may be emitted multiple times.
    """

    if language is None:
        language = 'en'

    for link in links:
        query = delta_query(link, source, target, language)
        res = endpoint.query(query)
        wd_links = [_link_from_wdsparql_row(row) for row in res]

        if (len(wd_links) == 1 and
           link.source in [wd_links[0].source, None] and
           link.target in [wd_links[0].target, None]):
            if link == wd_links[0]:
                yield [('=', wd_links[0])]
            else:
                yield [('~', wd_links[0])]
        else:
            # missing mapping
            # or different mapping: source OR target differ
            # or differnt mappings, one with other source, one with other target
            # or same mapping but different item (rare but possible)!
            delta = [('-', l) for l in wd_links]
            # indirect link with known QID => put QID into link
            if source is not None and len(delta) == 1:
                if delta[0][1].source == '' or delta[0][1].target == '':
                    link.annotation = delta[0][1].annotation
                    delta = []
            delta.insert(0, ('+', link))

            yield delta


def _link_from_wdsparql_row(row):
    qid = row['item'].split('/')[-1]
    if 'source' in row:
        return Link(row['source'], row['target'], qid)
    else:
        if row['annotation'] == qid:
            return Link(qid, row['target'], None)
        else:
            return Link(qid, row['target'], row['annotation'])

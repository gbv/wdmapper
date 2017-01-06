# -*- coding: utf-8 -*-
"""Access Wikidata."""

from __future__ import unicode_literals
import json
import sys

from .exceptions import WdmapperError
from .sparql import sparql_query
from .property import Property
from .link import Link


def get_property(p, cache=True, debug=False):
    """Get property data from Wikidata."""

    pid = Property.match(p)
    if pid:
        # get by property id
        uri = 'http://www.wikidata.org/entity/' + pid
        where = 'BIND(<' + uri + '> AS ?p)'
    elif Property.ns_pattern.match(p):
        # get by URL templateL (P1630)
        url = p + '$1' if p.find('$1') == -1 else p
        formatter_url = json.dumps(url)   # quote and escape literal
        where = '?p wdt:P1630 %s' % formatter_url
    else:
        # get by label
        label = json.dumps(p)           # quote and escape literal
        where = '?p rdfs:label ?l . FILTER (str(?l) = %s)' % label

    query = """\
            SELECT DISTINCT ?p ?label ?template ?pattern ?type WHERE {{
                {0} .
                ?p a wikibase:Property .
                ?p wikibase:propertyType ?type .
                OPTIONAL {{ ?p wdt:P1630 ?template }}
                OPTIONAL {{ ?p wdt:P1793 ?pattern }}
                SERVICE wikibase:label {{
                    bd:serviceParam wikibase:language "{1}" .
                    ?p rdfs:label ?label .
                }}
            }}""".format(where, 'en')

    properties = []
    for row in sparql_query(query, cache=cache, debug=debug):
        # filter out invalid properties. TODO: move to SPARQL query
        try:
            properties.append(Property(row))
        except WdmapperError:
            pass

    if not properties:
        raise WdmapperError('property not found: %s' % p)

    if len(properties) > 1:
        raise WdmapperError('multiple properties:\n' + '\n'.join(
                            ['{label} ({id})'.format(**p.__dict__)
                             for p in properties]))

    if debug:
        debug(repr(properties[0]))
    return properties[0]


def get_links(source, target, sort=False, limit=0, cache=True, debug=False, **args):
    """Get an iterator of links with given properties."""

    if source is None:
        query = """\
SELECT ?item ?target ?annotation WHERE {{
    ?item wdt:{target[id]} ?target .
    OPTIONAL {{ ?item rdfs:label ?annotation.
               FILTER(LANG(?annotation) = "en") }}
}}"""
        fields = '?target'
    else:
        query = """\
SELECT ?item ?source ?target WHERE {{
    ?item wdt:{source[id]} ?source .
    ?item wdt:{target[id]} ?target .
}}"""
        fields = '?source ?target'

    query = query.format(source=source, target=target)

    if (sort):
        query += '\nORDER BY ' + fields
    if (limit):
        query += '\nLIMIT {:d}'.format(limit)

    res = sparql_query(query, cache=cache, debug=debug)

    for row in res:
        yield _link_from_wdsparql_row(row)


def get_deltas(source, target, links, language='en', cache=True, debug=False, **args):
    """Check a list of links against Wikipedia and return deltas.

    A delta is a list of changes, each a tuple of operator (character) and link.
    In contrast to diffs, the same change may be emitted multiple times.
    """

    if source is None:
        sparql = """SELECT DISTINCT ?item ?target ?annotation WHERE {{
          {{
             BIND ("{target}" as ?target)
             {{ ?item wdt:{p_target} ?target }} UNION
             {{ BIND(<http://www.wikidata.org/entity/{source}> as ?item ) .
                ?item wdt:{p_target} ?target }}
            OPTIONAL {{ ?item rdfs:label ?annotation.
                       FILTER(LANG(?annotation) = "{language}") }}
          }}
        }}"""
    else:
        sparql = """SELECT DISTINCT ?source ?item ?target WHERE {{
          {{ {{ ?item wdt:{p_source} "{source}" }} UNION
             {{ ?item wdt:{p_target} "{target}" }} }}
          OPTIONAL {{ ?item wdt:{p_source} ?source }}
          OPTIONAL {{ ?item wdt:{p_target} ?target }}
        }}"""

    for link in links:
        query = sparql.format(source=link.source,
                              target=link.target,
                              p_source=source.id if source else None,
                              p_target=target.id,
                              language=language)
        res = sparql_query(query, cache=cache, debug=debug)
        wd_links = [_link_from_wdsparql_row(row) for row in res]

        if (len(wd_links) == 1 and
           wd_links[0].source == link.source and
           wd_links[0].target == link.target):
            if wd_links[0].annotation == link.annotation:
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
        return Link(qid, row['target'], row['annotation'])


def setup_pywikibot():
    """initialize pywikibot connected to wikidata

    File ``user-config.py`` (required by pywikibot) is created
    automatically, if needed.
    """

    global pywikibot
    global site
    global repo
    try:
        import pywikibot
    except RuntimeError as e:
        # create user-config.py if needed
        if os.path.exists('user-config.py'):
            raise
        # print('user-config.py created')
        file = open('user-config.py', 'w')
        file.write("\n".join([
            "mylang = 'wikidata'",
            "family = 'wikidata'",
            "# usernames['wikidata']['wikidata'] = u'YOUR-USERNAME'",
            "console_encoding = 'utf-8'", ""
        ]))
        file.close()
        import pywikibot
        site = pywikibot.Site()
        repo = site.data_repository()

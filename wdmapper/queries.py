# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def links_query(source, target, sort, limit, language, type):

    if not source or not hasattr(source,'id'):
        fields = '?target'
        query = """\
SELECT ?item ?target ?annotation WHERE {
    ?item wdt:%s ?target .
""" % (target.id)

        if language:
            query += """\
    SERVICE wikibase:label {
      bd:serviceParam wikibase:language "%s" .
      ?item rdfs:label ?annotation .
    }\n""" % language

    else:
        fields = '?source ?target'
        query = """\
SELECT ?item ?source ?target WHERE {
    ?item wdt:%s ?source .
    ?item wdt:%s ?target .
""" % (source.id, target.id)

    if type:
        query += '?item wdt:P31/wdt:P279* wd:%s' % (type)

    query += '}'

    if (sort):
        query += '\nORDER BY ' + fields
    if (limit):
        query += '\nLIMIT {:d}'.format(limit)

    return query


def delta_query(link, source, target, language):
    statements = []
    optional = ''

    # direct link
    if source is None:
        variables = '?item ?target ?annotation'

        if link.target is not None:
            statements.append("""
                { BIND ("%s" as ?target)
                  ?item wdt:%s ?target }
            """ % (link.target, target.id))

        if link.source is not None:
            statements.append("""
                { BIND(<http://www.wikidata.org/entity/%s> as ?item)
                  ?item wdt:%s ?target }
            """ % (link.source, target.id))

        if language:
            optional = """OPTIONAL {
                    ?item rdfs:label ?annotation.
                    FILTER(LANG(?annotation) = "%s")
                }""" % language

    # indirect link
    else:
        variables = '?item ?target ?source'

        if link.source is not None:
            statements.append('{ ?item wdt:%s "%s" }' % (source.id, link.source))

        if link.target is not None:
            statements.append('{ ?item wdt:%s "%s" }' % (target.id, link.target))

        optional += """
          OPTIONAL { ?item wdt:%s ?source }
          OPTIONAL { ?item wdt:%s ?target }
        """ % (source.id, target.id)

    statements = " UNION ".join(statements)
    return """
        SELECT DISTINCT %s WHERE {
            { %s }
            %s
        }""" % (variables, statements, optional)

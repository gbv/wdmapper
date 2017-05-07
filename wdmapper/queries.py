# -*- coding: utf-8 -*-
from __future__ import unicode_literals


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

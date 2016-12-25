# -*- coding: utf-8 -*-
"""Get and express information about Wikidata properties."""

from __future__ import unicode_literals
import re

from .exceptions import WdmapperError


class Property(object):
    """Information about a Wikidata property for authority file mapping.

    Attributes:
        uri (str): Full URI such as ``http://www.wikidata.org/entity/P227``
        id (str): Wikidata Property identifier such as ``P227``
        label (str): English primary label of the property
        template (str): URL template to link via identifiers of this property
        pattern (str): regular expression of identifier of this property

    Attributes can also be read as dictionary keys (e.g. ``p['uri'] == p.uri``)
    to facilitate access in formatting strings.
    """

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
        self.type = data.get('type')
        self.pattern = data.get('pattern')
        self.template = data.get('template')
        # type could also be: string, commons-media, globe-coordinate
        if self.type != 'http://wikiba.se/ontology#ExternalId':
            error = 'property {id} is not of type external-id!'
        elif not self.template:
            error = 'property {id} lacks URL template (P1630)'
        else:
            return
        raise WdmapperError(error.format(id=self.id))

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        s = "{label} ({id})\n<{uri}>\n{type}\n".format(**self.__dict__)
        if self.template:
            s += self.template
        s += "\n"
        if self.pattern:
            s += self.pattern
        return s

    @staticmethod
    def match(s):
        m = Property.id_pattern.match(s)
        if m:
            return 'P' + m.group('id')

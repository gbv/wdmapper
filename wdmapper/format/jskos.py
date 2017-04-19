# -*- coding: utf-8 -*-
"""JSKOS mapping writer."""

from __future__ import unicode_literals, print_function
import json
import six
from .base import LinkWriter

name = 'jskos'
extension = '.ndjson'


class Writer(LinkWriter):

    def expand_link(self, link, token, field):
        if field in self.meta and self.meta[field]:
            return {'uri': link.expand(token, self.meta[field])}
        else:
            return {'notation': link[token]}

    def write_link(self, link):
        fromSet = [self.expand_link(link, 'source', 'prefix')]
        toSet = [self.expand_link(link, 'target', 'target')]

        jskos = {
            'type': [self.mapping_type()],
            'from': {'memberSet': fromSet},
            'to': {'memberSet': toSet},
        }
        if self.meta['sourceset']:
            jskos['fromScheme'] = {'uri':self.meta['sourceset']}
        if self.meta['targetset']:
            jskos['toScheme'] = {'uri':self.meta['targetset']}

        self.print(six.u(json.dumps(jskos, self.stream, sort_keys=True)))

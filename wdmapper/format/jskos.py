# -*- coding: utf-8 -*-
"""JSKOS mapping writer."""

from __future__ import unicode_literals, print_function
import json
from ..writer import LinkWriter

name = 'jskos'
extension = '.ndjson'


class Writer(LinkWriter):

    def init(self, meta):
        self.meta = meta

    # TODO: DUPLCATED template replacing code may better be put elsewhere
    def expand_link(self, link, field):
        if field in self.meta and self.meta[field]:
            prefix = self.meta['prefix']
            if '$1' in prefix:
                uri = prefix.replace('$1', link.source)
            else:
                uri = prefix + link.source
            return {'uri': uri}
        else:
            return {'notation': link.source}

    def write_link(self, link):
        fromSet = [self.expand_link(link, 'prefix')]
        toSet = [self.expand_link(link, 'target')]

        jskos = {
            'type': [self.mapping_type()],
            'from': {'memberSet': fromSet},
            'to': {'memberSet': toSet},
        }
        if self.meta['sourceset']:
            jskos['fromScheme'] = {'uri':self.meta['sourceset']}
        if self.meta['targetset']:
            jskos['toScheme'] = {'uri':self.meta['targetset']}

        self.print(json.dumps(jskos, self.stream, sort_keys=True))

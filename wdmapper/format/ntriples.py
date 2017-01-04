# -*- coding: utf-8 -*-
"""RDF/NTriples writer."""

from __future__ import unicode_literals, print_function

from ..exceptions import WdmapperError

name = 'nt'
extension = '.nt'


class Writer:

    def __init__(self, stream, header=True):
        self.stream = stream
        self.meta = {}

    def init(self, meta):
        self.meta = meta

    def write_link(self, link):

        # TODO: template replacing code may better be put elsewhere
        if 'prefix' in self.meta:
            prefix = self.meta['prefix']
            if '$1' in prefix:
                s = prefix.replace('$1', link.source)
            else:
                s = prefix + link.source
        else:
            s = link.source

        if 'target' in self.meta:
            target = self.meta['target']
            if '$1' in target:
                o = target.replace('$1', link.target)
            else:
                o = target + link.target
        else:
            o = link.target

        if 'relation' in self.meta:
            p = self.meta['relation']
        if not p:
            p = 'http://www.w3.org/2004/02/skos/core#exactMatch'

        triple = map(lambda uri: '<%s>' % uri, [s,p,o])
        print(' '.join(triple), '.', file=self.stream)

    def write_delta(self, delta):  # TODO: move duplicated code to base class
        for op, link in delta:
            self.stream.write(op + ' ')
            self.write_link(link)

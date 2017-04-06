# -*- coding: utf-8 -*-
"""RDF/NTriples writer."""

from __future__ import unicode_literals, print_function
from ..writer import LinkWriter
from ..exceptions import WdmapperError

name = 'nt'
extension = '.nt'


class Writer(LinkWriter):

    def init(self, meta):
        self.meta = meta

    def write_link(self, link):

        # TODO: template replacing code may better be put elsewhere
        if 'prefix' in self.meta and self.meta['prefix']:
            prefix = self.meta['prefix']
            if '$1' in prefix:
                s = prefix.replace('$1', link.source)
            else:
                s = prefix + link.source
        else:
            s = link.source

        if 'target' in self.meta and self.meta['target']:
            target = self.meta['target']
            if '$1' in target:
                o = target.replace('$1', link.target)
            else:
                o = target + link.target
        else:
            o = link.target

        p = self.mapping_type()

        triple = map(lambda uri: '<%s>' % uri, [s,p,o])
        print(' '.join(triple), '.', file=self.stream)

    def write_delta(self, delta):  # TODO: move duplicated code to base class
        for op, link in delta:
            self.stream.write(op + ' ')
            self.write_link(link)

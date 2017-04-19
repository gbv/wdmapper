# -*- coding: utf-8 -*-
"""
Markdown writers for human-readable output.
"""

from __future__ import unicode_literals, print_function
import re
from .base import LinkReader, LinkWriter, DeltaWriter

name = 'markdown'
extension = '.md'


class Writer(LinkWriter, DeltaWriter):

    @classmethod
    def escape(cls, s):
        s = re.sub('[*\n{}]',' ', s)  # TODO: remove more special characters
        return s

    def start(self, meta):
        self.meta = meta
        if not self.header:
            return
        self.header = False

        self.print('# %s' % self.escape(meta['description']))
        self.print('')

    def write_link(self, link):
        if 'prefix' in self.meta and self.meta['prefix']:
            source = '[%s](%s)' % (link.source, link.expand('source', self.meta['prefix']))
        else:
            source = link.source
        if 'target' in self.meta and self.meta['target']:
            target = '[%s](%s)' % (link.target, link.expand('target', self.meta['target']))
        else:
            target = link.target
        md = '* %s ↔  %s' % (source, target)
        if link.annotation:
            md += ' (%s)' % self.escape(link.annotation)
        self.print(md)

    def write_delta(self, delta):
        for op, link in delta:
            self.print('* %s `%s`' % (op, link))

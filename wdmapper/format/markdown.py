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

    def source(self, link):
        if 'prefix' in self.meta and self.meta['prefix']:
            return '[%s](%s)' % (link.source, link.expand('source', self.meta['prefix']))
        else:
            return link.source

    def target(self, link):
        if 'target' in self.meta and self.meta['target']:
            return '[%s](%s)' % (link.target, link.expand('target', self.meta['target']))
        else:
            return link.target

    def annotation(self, link):
        if re.match('^Q[1-9][0-9]+$', link.annotation):
            return '[%s](http://www.wikidata.org/entity/%s)' % (link.annotation, link.annotation)
        else:
            return '"%s"' % self.escape(link.annotation)

    def write_link(self, link):
        if 'sourceproperty' in self.meta and 'targetproperty' in self.meta and self.meta['sourceproperty'] and self.meta['targetproperty']:
            md = '* %s ← %s →  %s' % (self.source(link), self.annotation(link), self.target(link))
        else:
            md = '* %s →  %s %s' % (self.source(link), self.target(link), self.annotation(link))
        self.print(md)

    def write_delta(self, delta):
        for op, link in delta:
            self.print('* %s `%s`' % (op, link))

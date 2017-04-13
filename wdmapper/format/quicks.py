# -*- coding: utf-8 -*-
"""
DeltaWriter for QuickStatements tool.

See https://tools.wmflabs.org/quickstatements/.
"""

from __future__ import unicode_literals, print_function

from .base import LinkReader, LinkWriter, DeltaWriter

name = 'quicks'


class Writer(DeltaWriter):

    def edit_link(self, link, command=''):
        if self.meta['sourceproperty']:  # indirect link
            qid = command + link.annotation
            prop = self.meta['sourceproperty']
            self.write_command((qid, prop, '"' + link.source + '"'))
            prop = self.meta['targetproperty']
            self.write_command((qid, prop, '"' + link.target + '"'))
        else:
            qid = command + link.source
            prop = self.meta['targetproperty']
            self.write_command((qid, prop, '"' + link.target + '"'))

    def write_command(self, parts):
        self.print('\t'.join(parts))

    def write_delta(self, delta):
        for op, link in delta:
            if op == '=':
                continue
            elif op == '~':
                if self.meta['sourceproperty']:  # indirect link
                    self.print("# skipping indirect link %s -> Q? -> %s" % (link.source, link.target))
                continue
            elif op == '+':
                self.edit_link(link,'')
            elif op == '-':
                self.edit_link(link,'-')

# -*- coding: utf-8 -*-
"""
DeltaWriter for QuickStatements tool.

See https://tools.wmflabs.org/quickstatements/.
"""

from __future__ import unicode_literals, print_function
import re
from .base import LinkReader, LinkWriter, DeltaWriter

name = 'quicks'


class Writer(DeltaWriter):

    def write_edit(self, link, prefix=''):
        targetprop = re.sub('.*/', '', self.meta['targetproperty'])
        if self.meta['sourceproperty']:
            qid = prefix + link.annotation
            sourceprop = re.sub('.*/', '', self.meta['sourceproperty'])
            self.statement(qid, sourceprop, link.source)
            self.statement(qid, targetprop, link.target)
        else:
            qid = prefix + link.source
            self.statement(qid, targetprop, link.target)

    def statement(self, qid, prop, value):
        self.print('%s\t%s\t"%s"' % (qid, prop, value))

    def skip(self, link):
        self.write_edit(link, '# ')

    def write_delta(self, delta):
        for op, link in delta:
            if link.source is None or link.target is None:
                # TODO: skip incomplete link
                continue

            if self.meta['sourceproperty']:
                if not re.match('^Q[1-9][0-9]+$', link.annotation):
                    self.skip(link)
                    continue
            else:
                if not re.match('^Q[1-9][0-9]+$', link.source):
                    self.skip(link)
                    continue

            if op == '=':
                continue
            elif op == '~':
                self.skip(link)
            elif op == '+':
                self.write_edit(link,'')
            elif op == '-':
                self.write_edit(link,'-')

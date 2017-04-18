# -*- coding: utf-8 -*-
"""
Markdown writers for human-readable output.
"""

from __future__ import unicode_literals, print_function

from .base import LinkReader, LinkWriter, DeltaWriter

name = 'markdown'
extension = '.md'


class Writer(LinkWriter, DeltaWriter):

    def write_link(self, link):
        self.print(link)

    def write_delta(self, delta):
        for op, link in delta:
            self.print('* %s %s' % (op, link))


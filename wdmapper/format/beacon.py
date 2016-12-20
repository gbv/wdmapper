# -*- coding: utf-8 -*-
"""BEACON link dump format writer."""

from __future__ import unicode_literals, print_function

import sys

from ..link import Link

PY3 = sys.version_info[0] == 3
if PY3:
    text_type = str
else:
    text_type = unicode


meta_fields = ['name', 'description', 'prefix', 'target',
               'creator', 'contact', 'homepage', 'feed', 'timestamp', 'update'
               'sourceset', 'targetset', 'institution',
               'relation', 'message', 'annotation']


def writer(stream, **meta):
    """Return a new Writer instance."""
    return Writer(stream, **meta)


class Writer:

    def __init__(self, stream, header=True, **meta):
        self.stream = stream
        self.meta = meta
        if header:
            self.write_header()

    def print(self, s):
        print(s, file=self.stream)

    def write_header(self):
        self.print('#FORMAT: BEACON')
        for key in meta_fields:
            if key in self.meta and self.meta[key] is not None:
                value = self.meta[key]
                if isinstance(value, text_type):
                    value = [value]
                for v in value:
                    self.print('#%s: %s' % (key.upper(), v))
        self.print('')

    def write_link(self, link):
        row = [link.source]

        # TODO: omit if possible
        row.append(link.annotation)
        row.append(link.target)

        self.print('|'.join(row))

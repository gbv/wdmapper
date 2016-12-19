# -*- coding: utf-8 -*-
"""BEACON link dump format writer."""

from __future__ import unicode_literals, print_function

meta_fields = ['name', 'description', 'prefix', 'target',
               'creator', 'contact', 'homepage', 'feed', 'timestamp', 'update'
               'sourceset', 'targetset', 'institution',
               'relation', 'message', 'annotation']


def writer(stream, **meta):
    """Return a new Writer instance."""
    return Writer(stream, **meta)


class Writer:

    def __init__(self, stream, **meta):
        self.stream = stream
        self.meta = meta
        self.write_header()

    def print(self, s):
        print(s, file=self.stream)

    def write_header(self):
        self.print('#FORMAT: BEACON')
        for key in meta_fields:
            if key in self.meta and self.meta[key] is not None:
                value = self.meta[key]
                if isinstance(value, list):
                    value = [value]
                for v in value:
                    self.print('#%s: %s' % (key.upper(), v))
        self.print('')

    def write_link(self, link):
        row = [link['source']]

        # TODO: omit if possible
        if 'annotation' in link and link['annotation'] is not None:
            row.append(link['annotation'])
        else:
            row.append('')

        if 'target' in link and link['target'] is not None:
            row.append(link['target'])
        else:
            row.append('')

        self.print('|'.join(row))

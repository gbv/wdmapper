# -*- coding: utf-8 -*-
"""BEACON link dump format writer."""

from __future__ import unicode_literals, print_function

import sys
import re

from ..link import Link
from ..exceptions import WdmapperError

PY3 = sys.version_info[0] == 3
if PY3:
    text_type = str
else:
    text_type = unicode


meta_fields = ['name', 'description', 'prefix', 'target',
               'creator', 'contact', 'homepage', 'feed', 'timestamp', 'update'
               'sourceset', 'targetset', 'institution',
               'relation', 'message', 'annotation']

name = 'beacon'

extension = '.txt'
"""extension of BEACON files."""


def writer(stream, **meta):
    """Return a new Writer instance."""
    return Writer(stream, **meta)


class Writer:

    def __init__(self, stream, header=True):
        self.stream = stream
        self.initialized = header is False

    def print(self, s):
        print(s, file=self.stream)

    def init(self, meta):
        if self.initialized:
            return
        self.initialized = True
        self.print('#FORMAT: BEACON')
        for key in meta_fields:
            if key in meta and meta[key] is not None:
                value = meta[key]
                if isinstance(value, text_type):
                    value = [value]
                for v in value:
                    if key.upper() in ['PREFIX', 'TARGET']:
                        # BEACON template syntax uses '{ID}' instead of '$1'
                        v = re.sub(r'{ID}$','', v.replace('$1','{ID}'))
                    self.print('#%s: %s' % (key.upper(), v))
        self.print('')

    def write_link(self, link):
        if not self.initialized:
            raise WdmapperError(str(self.__class__) +
                                " instance not initialized!")
        row = [link.source]

        # TODO: omit if possible
        row.append(link.annotation)
        row.append(link.target)

        self.print('|'.join(row))

    def write_delta(self, delta):  # TODO: move duplicated code to base class
        for op, link in delta:
            self.stream.write(op + ' ')
            self.write_link(link)

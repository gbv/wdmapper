# -*- coding: utf-8 -*-
"""BEACON link dump format writer."""

from __future__ import unicode_literals, print_function

import functools
from itertools import chain
import sys
import re

from .base import LinkReader, LinkWriter, DeltaWriter

from ..link import Link
from ..exceptions import WdmapperError

PY3 = sys.version_info[0] == 3
if PY3:
    text_type = str
else:
    text_type = unicode


meta_fields = ['name', 'description', 'prefix', 'target',
               'creator', 'contact', 'homepage', 'feed', 'timestamp', 'update',
               'sourceset', 'targetset', 'institution',
               'relation', 'message', 'annotation']

name = 'beacon'
extension = '.txt'


class Reader(LinkReader):

    def start(self):
        stream = iter(self.stream.readline, '')  # support streaming input

        # read meta lines
        for line in stream:
            if line[0] == '#':
                key, value = line[1:].split(':',1)  # TODO: split at : or space or tab
                key = key.strip()
                if re.match('^[A-Z]+$', key):
                    self.meta[key.lower()] = value.strip()
            else:
                self.stream = chain([line], stream)  # push back
                break

    def next(self):
        """Read link lines and generate links from link tokens."""
        for line in self.stream:
            line = line.strip()
            token = line.split('|')
            if len(token) == 1:
                yield Link(source=token[0])
            elif len(token) == 2:
                # TODO: support alternative syntax
                # TODO: could be empty link!
                yield Link(source=token[0], annotation=token[1])
            else:
                yield Link(source=token[0], annotation=token[1], target=token[2])


class Writer(LinkWriter, DeltaWriter):

    def start(self, meta):
        if self.started:
            return
        self.started = True
        if not self.header:
            return
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
        if not self.started:
            raise WdmapperError(str(self.__class__) + " instance not started!")

        token = ['' if s is None else s for s in
                 [link.source, link.annotation, link.target]]

        if token[2] in ['', token[1]]:  # target missing or equal to source
            token.pop()

        if token:
            if len(token) == 2 and token[0] == token[1]:  # source == target
                token.pop()
            self.print('|'.join(token))

    def write_delta(self, delta):
        for op, link in delta:
            self.stream.write(op + ' ')
            self.write_link(link)

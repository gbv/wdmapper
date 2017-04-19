# -*- coding: utf-8 -*-
"""BEACON link dump format writer."""

from __future__ import unicode_literals, print_function

import functools
from itertools import chain
import sys
import re
import six

from .base import LinkReader, LinkWriter, DeltaWriter

from ..link import Link
from ..exceptions import WdmapperError


meta_fields = ['name', 'description', 'prefix', 'target',
               'creator', 'contact', 'homepage', 'feed', 'timestamp', 'update',
               'sourceset', 'targetset', 'institution',
               'sourceproperty', 'targetproperty',
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
                value = value.strip()
                if re.match('^[A-Z]+$', key):
                    key = key.lower()
                    if key in ['prefix', 'target']:
                        if '{ID}' in value:
                            value = value.replace('{ID}','$1')
                        else:
                            value = value + '$1'
                    self.meta[key] = value

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
                if isinstance(value, six.text_type):
                    value = [value]
                for v in value:
                    if key.upper() in ['PREFIX', 'TARGET']:
                        # BEACON template syntax uses '{ID}' instead of '$1'
                        v = re.sub(r'{ID}$','', v.replace('$1','{ID}'))
                    self.print('#%s: %s' % (key.upper(), v))
        self.print('')

    def write_link(self, link):
        token = ['' if s is None else s for s in link.tokens()]
        token = [token[0], token[2], token[1]]  # source, annotation, target

        if token[2] in ['', token[0]]:  # target missing or equal to source
            token.pop()
            if token[1] == '':          # no annotation
                token.pop()

        self.print('|'.join(token))

    def write_delta(self, delta):
        for op, link in delta:
            self.stream.write(op + ' ')
            self.write_link(link)

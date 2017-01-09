# -*- coding: utf-8 -*-
"""BEACON link dump format writer."""

from __future__ import unicode_literals, print_function

import sys
import re

from ..writer import LinkWriter
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


class Writer(LinkWriter):

    def __init__(self, stream, header=True):
        self.stream = stream
        self.initialized = header is False

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

        token = ['' if s is None else s for s in
                 [link.source, link.annotation, link.target]]

        if token[2] in ['', token[1]]:  # target missing or equal to source
            token.pop()

        if token:
            if len(token) == 2 and token[0] == token[1]:  # source == target
                token.pop()
            self.print('|'.join(token))

# -*- coding: utf-8 -*-
"""CSV format reader and writer."""

from __future__ import unicode_literals, absolute_import, print_function

import csv
import json
import sys

from .base import LinkReader, LinkWriter

from ..link import Link
from ..exceptions import WdmapperError

CSV_FIELDS = ['source', 'target', 'annotation']

name = 'csv'
extension = '.csv'

PY3 = sys.version_info[0] == 3


def _unicode_csv_reader(unicode_csv_data, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    def utf_8_encoder(unicode_csv_data):
        for line in unicode_csv_data:
            yield line.encode('utf-8')
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data), **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]


class Reader(LinkReader):
    """Read Links in CSV format."""

    def start(self):
        stream = iter(self.stream.readline, '')  # support streaming input

        if PY3:
            self.csv_reader = csv.reader(stream, skipinitialspace=True)
        else:
            self.csv_reader = _unicode_csv_reader(stream, skipinitialspace=True)

        self.header_row = None if self.header else CSV_FIELDS
        self.line = 0

    def links(self):
        return [l for l in self.next() if l]

    def next(self):
        for row in self.csv_reader:
            self.line = self.line + 1
            if self.header_row:
                # TODO: simplify this
                mapping = []
                mapping = {k: v for k, v in zip(self.header_row, row) if v != ''}
                try:
                    try:
                        link = Link(source=mapping['source'])
                    except (ValueError, KeyError):
                        # raise WdmapperError('missing source in line %d' % line)
                        link = Link('')
                    if 'target' in mapping:
                        link.target = mapping['target']
                    if 'annotation' in mapping:
                        link.annotation = mapping['annotation']
                    if link:
                        yield link
                except ValueError:
                    pass
            else:
                self.header_row = row


class Writer(LinkWriter):
    """
    Writes Links in CSV format.

    The csv module does not support Unicode so do we create CSV by hand.
    """

    separator = ', '
    escaped = [',','"']

    @classmethod
    def escape(cls, s):
        if s is None:
            return ''
        else:
            # always remove newlines and tab and trim whitespace
            s = s.rstrip('\r\n\t').strip()
            if cls.separator in s or '"' in s:
                s = json.dumps(s).replace('\\"','""')
            return s

    def start(self, meta):
        self.started = True
        if self.header:
            self.write_link(Link('source', 'target', 'annotation'))

    def write_link(self, link):
        if not self.started:
            raise WdmapperError(str(self.__class__) + " instance not started!")

        row = []
        for key in CSV_FIELDS:
            row.append(self.escape(getattr(link,key)))

        if row[-1] == '':   # omit annotation if empty
            row.pop()

        self.print(self.separator.join(row))

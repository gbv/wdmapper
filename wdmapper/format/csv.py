# -*- coding: utf-8 -*-
"""CSV format reader and writer."""

from __future__ import unicode_literals, absolute_import, print_function

import csv
import json
import sys

from ..link import Link
from ..exceptions import WdmapperError

CSV_FIELDS = ['source', 'target', 'annotation']

name = 'csv'

extension = '.csv'
"""extension of CSV files."""


def reader(stream, header=True):
    """Read mappings in CSV format."""

    if (header):
        header_row = None
    else:
        header_row = CSV_FIELDS

    stream = iter(stream.readline, '')  # support streaming input

    if sys.version_info[0] > 2:
        csv_reader = csv.reader(stream, skipinitialspace=True)
    else:
        csv_reader = unicode_csv_reader(stream, skipinitialspace=True)
    for row in csv_reader:
        if header_row:
            # TODO: simplify this
            mapping = []
            mapping = {k: v for k, v in zip(header_row, row) if v != ''}
            try:
                link = Link(mapping['source'])
                if 'target' in mapping:
                    link.target = mapping['target']
                if 'annotation' in mapping:
                    link.annotation = mapping['annotation']
                yield link
            except ValueError:
                pass
        else:
            header_row = row


def unicode_csv_reader(unicode_csv_data, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data), **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]


def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


def writer(stream, header=True):
    """Return a new CSV Writer instance."""
    return Writer(stream, header)


class Writer:
    """
    Writes Links in CSV format.

    The csv module does not support Unicode so do we create CSV by hand.
    """

    separator = ', '
    escaped = [',','"']

    @classmethod
    def escape(cls, s):
        # always remove newlines and tab and trim whitespace
        s = s.rstrip('\r\n\t').strip()
        if cls.separator in s or '"' in s:
            s = json.dumps(s).replace('\\"','""')
        return s

    def __init__(self, stream, header=True):
        self.stream = stream
        self.header = header
        self.initialized = header is False

    def init(self, meta):
        if self.initialized:
            return
        self.initialized = True
        if self.header:
            self.write_link(Link('source', 'target', 'annotation'))

    def write_link(self, link):
        if not self.initialized:
            raise WdmapperError(str(self.__class__) +
                                " instance not initialized!")

        row = []
        for key in CSV_FIELDS:
            row.append(self.escape(getattr(link,key)))

        if row[-1] == '':   # omit annotation if empty
            row.pop()

        print(self.separator.join(row), file=self.stream)

    def write_delta(self, delta):  # TODO: move duplicated code to base class
        for op, link in delta:
            self.stream.write(op + ' ')
            self.write_link(link)

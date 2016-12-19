# -*- coding: utf-8 -*-
"""CSV format reader and writer."""

from __future__ import unicode_literals, absolute_import, print_function

import csv
import json
import sys

CSV_FIELDS = ['source', 'target', 'annotation']


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
            mapping = []
            mapping = {k: v.strip() for k, v in zip(header_row, row) if v != ''}
            yield mapping
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

    def __init__(self, stream, header):
        self.stream = stream
        if (header):
            self.write_link(dict(zip(CSV_FIELDS, CSV_FIELDS)))

    def write_link(self, link):
        row = []
        for key in CSV_FIELDS:
            if key in link and link[key] is not None:
                row.append(self.escape(link[key]))
            else:
                row.append('')

        if row[-1] == '':   # omit annotation if empty
            row.pop()

        print(self.separator.join(row), file=self.stream)

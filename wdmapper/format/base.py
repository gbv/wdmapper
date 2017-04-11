# -*- coding: utf-8 -*-
"""Abstract base class of readers and writers."""

from __future__ import unicode_literals, print_function


class LinkReader:

    def __init__(self, stream, header=True):
        self.stream = stream
        self.header = header
        self.meta = {}

    def start():
        pass

    def next(self):
        raise NotImplementedError()

    def links(self):
        return [l for l in self.next() if l]


class LinkWriter:

    def __init__(self, stream, header=True):
        self.stream = stream
        self.meta = {}

    def mapping_type(self):
        if 'relation' in self.meta and self.meta['relation']:
            return self.meta['relation']
        else:
            return 'http://www.w3.org/2000/01/rdf-schema#seeAlso'

    def print(self, s):
        """Print a string without buffering."""
        print(s, file=self.stream)
        try:
            self.stream.flush()
        except IOError:  # raised for instance if stream has been closed
            pass


class DeltaWriter:

    def write_delta(self, delta):
        raise NotImplementedError()

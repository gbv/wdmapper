# -*- coding: utf-8 -*-
"""Abstract base classes to define readers and writers."""

from __future__ import unicode_literals, print_function
from abc import ABCMeta, abstractmethod


class LinkReader:
    """Abstract reader of links."""
    __metaclass__ = ABCMeta

    def __init__(self, stream, header=True):
        self.stream = stream
        self.header = header
        self.meta = {}

    def start():
        pass

    @abstractmethod
    def next(self):
        pass

    def links(self):
        return [l for l in self.next() if l]


class Writer:
    """Abstract writer of links or deltas."""
    __metaclass__ = ABCMeta

    def __init__(self, stream, header=True):
        """Create a new writer."""
        self.stream = stream
        self.header = header
        self.meta = {}
        self.started = False

    def start(self, meta):
        """Start writing with given metadata."""
        self.meta = meta

    def print(self, s):
        """Helper method to print a string without buffering."""

        print(s, file=self.stream)
        try:
            self.stream.flush()
        except IOError:  # raised for instance if stream has been closed
            pass


class LinkWriter(Writer):
    """Abstract writer of links."""
    __metaclass__ = ABCMeta

    # TODO: move to meta class
    def mapping_type(self):
        if 'relation' in self.meta and self.meta['relation']:
            return self.meta['relation']
        else:
            return 'http://www.w3.org/2000/01/rdf-schema#seeAlso'


class DeltaWriter(Writer):
    """Abstract writer of deltas."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def write_delta(self, delta):
        pass

# -*- coding: utf-8 -*-
"""Abstract writer base class to implement output formats."""

from __future__ import unicode_literals, print_function


class LinkWriter:

    def print(self, s):
        """Print a string without buffering."""
        print(s, file=self.stream)
        try:
            self.stream.flush()
        except IOError:  # raised for instance if stream has been closed
            pass

    def write_delta(self, delta):
        for op, link in delta:
            self.stream.write(op + ' ')
            self.write_link(link)

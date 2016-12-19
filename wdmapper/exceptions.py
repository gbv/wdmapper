# -*- coding: utf-8 -*-
"""Exceptions raised by wdmapper."""

from __future__ import unicode_literals, print_function
import sys


class WdmapperError(Exception):
    """Basic exception for errors raised by wdmapper"""

    def message(self):
        return self.args[0]


class ArgumentError(WdmapperError):

    def __init__(self, name, allow=None, got=None):
        self.name = name
        self.allow = allow
        self.got = got

    def message(self):
        if self.allow:
            return self.name + ' must be one of: ' + ', '.join(self.allow)
        elif self.got is not None:
            return self.name + 'is is missing'
        else:
            return 'invalid ' + self.name

# -*- coding: utf-8 -*-
"""Exceptions raised by wdmapper."""

from __future__ import print_function
import sys


class WdmapperError(Exception):
    """Basic exception for errors raised by wdmapper"""

    def print_and_exit(self):
        """Print error message to STDERR and exit with error code."""
        print(self.args[0], file=sys.stderr)
        sys.exit(1)

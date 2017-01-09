# -*- coding: utf-8 -*-
"""BEACON link element consisting of source, target, and annotation token."""

from __future__ import unicode_literals

from functools import total_ordering
import re
import sys

if sys.version_info[0] == 3:  # PY3
    text_type = str
else:
    text_type = unicode


@total_ordering
class Link(object):
    """
    BEACON link element.

    A Link element consists of three tokens

    * a source token (mandatoy in most applications)
    * an optional target token
    * an optional annotation token

    All tokens are witespace-normalized (as defined by BEACON) Unicode strings.
    An empty string is equal to a missing token (value ``None``).

    Link objects can be compared, represented with repr(), and hashed for
    set-operations.
    """

    @staticmethod
    def whitespace_normalize(value):
        if value is not None:
            if not isinstance(value, text_type):
                raise ValueError('Link token must be Unicode string')
            value = re.sub('[\n\r\t ]+', ' ', value.strip('\n\r\t '))
            if value == '':
                value = None
        return value

    def __init__(self, source, target=None, annotation=None):
        self.source = source
        self.target = target
        self.annotation = annotation
        self._hash = None

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = Link.whitespace_normalize(value)

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = Link.whitespace_normalize(value)

    @property
    def annotation(self):
        return self._annotation

    @annotation.setter
    def annotation(self, value):
        self._annotation = Link.whitespace_normalize(value)

    def tokens(self):
        return (self._source, self._target, self._annotation)

    def __bool__(self):
        return not all(True if t is None else False for t in self.tokens())

    __nonzero__ = __bool__

    def __lt__(self, other):
        return self.tokens() < other.tokens()

    def __eq__(self, other):
        return self.tokens() == other.tokens()

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(self.tokens())
        return self._hash

    def __repr__(self):
        args = [repr(self._source)]
        if self._target is not None:
            args.append(repr(self._target))
            if self._annotation is not None:
                args.append(repr(self._annotation))
        elif self._annotation is not None:
            args.append('annotation=' + repr(self._annotation))
        return 'Link(' + ', '.join(args) + ')'

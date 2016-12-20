# -*- coding: utf-8 -*-
"""BEACON link element consisting of source, target, and annotation token."""

from __future__ import unicode_literals

from functools import total_ordering
import re
import sys

PY3 = sys.version_info[0] == 3
if PY3:
    text_type = str
else:
    text_type = unicode


@total_ordering
class Link(object):
    """
    BEACON link element.

    A Link element consists of three tokens

    * a mandatory source token
    * an optional target token
    * an optional annotation token

    All tokens are witespace-normalized (as defined by BEACON) Unicode strings.
    A missing token is equal to the empty string.

    Link objects can be compared, represented with repr(), and hashed for
    set-operations.
    """

    @staticmethod
    def whitespace_normalize(value):
        if value is None:
            return ''
        if not isinstance(value, text_type):
            raise ValueError('Link token must be Unicode string')
        value = value.strip('\n\r\t ')
        return re.sub('[\n\r\t ]+', ' ', value)

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
        value = Link.whitespace_normalize(value)
        if value == '':
            raise ValueError('Link source must not be empty')
        else:
            self._source = value

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
        if self._target != "":
            args.append(repr(self._target))
            if self._annotation != "":
                args.append(repr(self._annotation))
        elif self._annotation != "":
            args.append('annotation=' + repr(self._annotation))
        return 'Link(' + ', '.join(args) + ')'

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
import collections

from wdmapper.link import Link


def test_constructor():
    l = Link(' f\r\t\n ö\n', annotation=None)
    assert l.source == 'f ö'
    assert l.target == ''
    assert l.annotation == ''


def test_exception():
    l = Link('foo', 'bar')
    l.source = None
    assert l.valid() is False
    with pytest.raises(ValueError):
        l.target = []


def test_repr():
    l = Link('foo', 'bar')
    assert repr(l) == "Link(%s, %s)" % (repr('foo'), repr('bar'))
    l.annotation = 'x'
    assert repr(l) == "Link(%s, %s, %s)" % (repr('foo'), repr('bar'), repr('x'))
    l.target = None
    assert repr(l) == "Link(%s, annotation=%s)" % (repr('foo'), repr('x'))


def test_compare():
    a = Link('a','a','a')
    b = Link('a','a','b')
    assert a != b
    assert a <= b
    b.annotation = 'a'
    assert a == b


def test_sets():
    a = Link('foo', 'bar', 'doz')
    b = Link('foo', 'bar', 'doz')
    c = Link('42')

    assert isinstance(a, collections.Hashable)
    assert hash(a) == hash(b)
    assert hash(b) != hash(c)

    s1 = set([a])
    s2 = set([b])
    s3 = set([c])

    assert (s1 - s2) == set()
    assert (s1 | s2) == set([a])
    assert (s1 | s2 | s3) == set([a,b,c])
    assert ((s1 | s2 | s3) - s1) == set([c])

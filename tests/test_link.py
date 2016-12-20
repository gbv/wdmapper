# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from wdmapper.link import Link


def test_constructor():
    l = Link(' f\r\t\n ö\n', annotation=None)
    assert l.source == 'f ö'
    assert l.target == ''
    assert l.annotation == ''


def test_exception():
    l = Link('foo', 'bar')
    with pytest.raises(ValueError):
        l.source = None
    assert l.source == 'foo'
    assert l.target == 'bar'
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

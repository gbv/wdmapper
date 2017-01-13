# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
import io

from wdmapper.format import beacon
from wdmapper.link import Link


def test_write_no_header():
    out = io.StringIO('')
    writer = beacon.Writer(out, header=False)
    writer.write_link(Link('foo', 'b"r'))
    assert out.getvalue() == 'foo||b"r\n'


def test_reader():
    tests = {
        '': ({},[]),
        ' |\t|  ': ({},[]),
        'foo|bar': ({},[Link(source='foo',annotation='bar')]),
        ' foo  ||\tbar ': ({},[Link(source='foo',target='bar')]),
        'foo|bar|doz|baz': ({},[Link('foo','doz',annotation='bar')]),
        '#TARGET:  foo\nx': ({'target':'foo'},[Link('x')]),
        'x\ny\nz': ({},[Link(s) for s in ['x','y','z']]),
    }

    for string, expect in tests.items():
        reader = beacon.Reader(io.StringIO(string))
        meta, links = reader.read()
        assert meta == expect[0]
        assert list(links) == expect[1]

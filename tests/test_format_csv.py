# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
import io

from wdmapper.format import csv
from wdmapper.link import Link


def test_read():
    s = ' fö\t, "b""r"\n'
    data = csv.Reader(io.StringIO(s), header=True).links()
    assert list(data) == []

    data = csv.Reader(io.StringIO(s), header=False).links()
    assert list(data) == [Link('fö', 'b"r')]

    s = 'target, source\nbar, foo\n , \ndoz'
    data = csv.Reader(io.StringIO(s), header=True).links()
    assert list(data) == [Link('foo','bar'),Link(None,'doz')]


def test_write():
    out = io.StringIO("")
    writer = csv.Writer(out, header=True)
    writer.init({})
    assert out.getvalue() == "source, target, annotation\n"

    writer.write_link(Link('foo','b"r'))
    assert out.getvalue() == 'source, target, annotation\nfoo, "b""r"\n'

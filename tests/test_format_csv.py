# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
import io

from wdmapper.format import csv
from wdmapper.link import Link


def test_read():
    s = ' fö\t, "b""r"\n'
    reader = csv.Reader(io.StringIO(s), header=True)
    reader.start()
    assert list(reader.links()) == []

    reader = csv.Reader(io.StringIO(s), header=False)
    reader.start()
    assert list(reader.links()) == [Link('fö', 'b"r')]

    s = 'target, source\nbar, foo\n , \ndoz'
    reader = csv.Reader(io.StringIO(s), header=True)
    reader.start()
    assert list(reader.links()) == [Link('foo','bar'),Link(None,'doz')]


def test_write():
    out = io.StringIO("")
    writer = csv.Writer(out, header=True)
    writer.start({})
    assert out.getvalue() == "source, target, annotation\n"

    writer.write_link(Link('foo','b"r'))
    assert out.getvalue() == 'source, target, annotation\nfoo, "b""r"\n'

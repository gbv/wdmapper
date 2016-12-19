# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
import io

from wdmapper.format import csv


def test_read():
    s = ' fö\t, "b""r"\n'
    data = csv.reader(io.StringIO(s), header=True)
    assert list(data) == []

    data = csv.reader(io.StringIO(s), header=False)
    assert list(data) == [{'source':'fö','target':'b"r'}]


def test_write():
    out = io.StringIO("")
    writer = csv.writer(out, header=True)
    assert out.getvalue() == "source, target, annotation\n"

    writer.write_link({'source':'foo','target':'b"r'})
    assert out.getvalue() == 'source, target, annotation\nfoo, "b""r"\n'

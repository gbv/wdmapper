# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
import io

from wdmapper.format import beacon
from wdmapper.link import Link


def test_write():
    out = io.StringIO('')
    writer = beacon.writer(out)
    metalines = out.getvalue()
    writer.write_link(Link('foo', 'b"r'))
    assert out.getvalue() == metalines + 'foo||b"r\n'

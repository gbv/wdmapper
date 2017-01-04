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

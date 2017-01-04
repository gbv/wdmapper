# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from wdmapper import wdmapper


def test_csv_to_beacon(capsys):
    wdmapper('convert', input='tests/simple.csv', to='beacon', relation='owl:sameAs')
    out, err = capsys.readouterr()
    assert out == """\
#FORMAT: BEACON
#RELATION: http://www.w3.org/2002/07/owl#sameAs

xyz|☃|123
"""

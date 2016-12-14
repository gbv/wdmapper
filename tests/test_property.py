# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytest

from re import match
from wdmapper import run


def test_property(capsys):
    run('P214')
    out, err = capsys.readouterr()
    assert out.startswith("""\
VIAF ID (P214)
<http://www.wikidata.org/entity/P214>
https://viaf.org/viaf/$1
[1-9]""")


def test_property_not_found(capsys):
    with pytest.raises(SystemExit):
        run('Ä')
    out, err = capsys.readouterr()
    assert match('^property not found: Ä', err)

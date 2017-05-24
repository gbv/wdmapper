# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytest
from re import match

from wdmapper.cli import run
from wdmapper.property import Property


def test_property_match():
    pid = Property.match('http://www.wikidata.org/entity/P123')
    assert pid == 'P123'


def test_property(capsys):
    run('P214')
    out, err = capsys.readouterr()
    assert out.startswith("""\
#FORMAT: BEACON
#NAME: VIAF ID
#DESCRIPTION: Mapping from Wikidata IDs to VIAF IDs
#PREFIX: http://www.wikidata.org/entity/
#TARGET: http://viaf.org/viaf/
""")


def test_property_not_found(capsys):
    with pytest.raises(SystemExit):
        run('Ä')
    out, err = capsys.readouterr()
    assert match('^property not found: Ä', err)

# -*- coding: utf-8 -*-
"""Test functions and variables exported from wdmapper.format."""

from __future__ import unicode_literals

import pytest
from wdmapper.format import *
from wdmapper.format.base import LinkReader, LinkWriter, DeltaWriter


def test_readers():
    names = ['beacon','csv']
    assert sorted(readers.keys()) == names
    for name in names:
        assert issubclass(type(readers[name]), type(LinkReader))


def test_writers():
    names = ['beacon','csv', 'jskos', 'nt', 'quicks']
    assert sorted(writers.keys()) == names
    for name in names:
        assert issubclass(type(writers[name]), type(LinkWriter))


def test_guess_format():
    assert guessFormat('foo.txt', readers.keys()) == 'beacon'
    assert guessFormat('foo.ndjson', writers.keys()) == 'jskos'
    assert guessFormat('foo.csv') == 'csv'
    assert guessFormat('foo.nt') == 'nt'

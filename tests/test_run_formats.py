# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
import io
import sys
import codecs
import functools

from wdmapper.cli import run


def slurp(filename):
    with codecs.open(filename, 'r', encoding='utf8') as f:
        return f.read()


def test_read_csv_stdin(stdin, capsys):
    with stdin("föö,bar\n"):
        run('convert', '-H', '-t', 'csv')
    out, err = capsys.readouterr()
    expect = "föö, bar\n"
    assert out == expect


def test_read_csv_file(capsys):
    run('convert', '-i', 'tests/simple.csv', '-t', 'csv')
    out, err = capsys.readouterr()
    expect = "source, target, annotation\nxyz, 123, ☃\n"
    assert out == expect


def test_csv_to_beacon_as_default(capsys):
    run('convert', '-i', 'tests/simple.csv')
    out, err = capsys.readouterr()
    assert out == slurp('tests/simple.txt')


def test_csv_to_beacon(capsys):
    run('convert', '-i', 'tests/simple.csv', '-t', 'beacon')
    out, err = capsys.readouterr()
    assert out == slurp('tests/simple.txt')


def test_csv_to_jskos(capsys):
    run('convert', '-i', 'tests/simple.csv', '-t', 'jskos')
    out, err = capsys.readouterr()
    assert out == slurp('tests/simple.ndjson')

 
def test_unknown_format(capsys):
    with pytest.raises(SystemExit):
        run('-f', 'xxx')
    out, err = capsys.readouterr()
    assert err.startswith('input format must be one of: ')

    with pytest.raises(SystemExit):
        run('-t', 'xxx')
    out, err = capsys.readouterr()
    assert err.startswith('output format must be one of: ')

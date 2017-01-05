# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
import io
import sys

from wdmapper.cli import run


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
    assert out.startswith('#FORMAT: BEACON\n')


def test_csv_to_beacon(capsys):
    run('convert', '-i', 'tests/simple.csv', '-t', 'beacon')
    out, err = capsys.readouterr()
    expect = "#FORMAT: BEACON\n\nxyz|☃|123\n"
    assert out == expect


def test_unknown_format(capsys):
    with pytest.raises(SystemExit):
        run('-f', 'xxx')
    out, err = capsys.readouterr()
    assert err.startswith('input format must be one of: ')

    with pytest.raises(SystemExit):
        run('-t', 'xxx')
    out, err = capsys.readouterr()
    assert err.startswith('output format must be one of: ')


def test_missing_source(stdin, capsys):
    with pytest.raises(SystemExit):
        with stdin('source,target\n,bar\n'):
            run('convert', '-t', 'csv')
    out, err = capsys.readouterr()
    assert out == 'source, target, annotation\n'
    assert err == 'missing source in line 2\n'


def test_missing_target(stdin, capsys):
    with pytest.raises(SystemExit):
        with stdin("foo,\n"):
            run('convert', '-H', '-t', 'csv')
    out, err = capsys.readouterr()
    assert out == ''
    assert err == 'missing target in line 1\n'

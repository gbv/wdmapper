# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
import io
import sys

from wdmapper.cli import run


# TODO: put this into test fixture file
@pytest.fixture
def stdin():
    return lambda s: MockStdin(s)


class MockStdin:
    def __init__(self, data):
        self.data = data
        self.stdin = sys.stdin

    def __enter__(self):
        if sys.version_info[0] == 3:
            # Python 3: sys.stdin is unicode
            sys.stdin = io.StringIO(self.data)
        else:
            # Python 2: sys.stdin is bytes (UTF-8)
            sys.stdin = io.BytesIO(self.data.encode('utf-8'))

    def __exit__(self, type, value, traceback):
        sys.stdin = self.stdin


def test_read_csv_stdin(stdin, capsys):
    with stdin("föö,bar\n"):
        run('convert', '-H')
    out, err = capsys.readouterr()
    expect = "föö, bar\n"
    assert out == expect


def test_read_csv_file(capsys):
    run('convert', '-i', 'tests/simple.csv')
    out, err = capsys.readouterr()
    expect = "source, target, annotation\nxyz, 123, ☃\n"
    assert out == expect


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

import pytest
import io
import sys

from wdmapper import run


def test_read_csv_stdin(capsys):
    input = io.StringIO(u"foo,bar\n")
    sys.stdin = input
    run('echo', '-H')
    out, err = capsys.readouterr()
    expect = u"foo | bar\n"
    assert out == expect


def test_read_csv_file(capsys):
    run('echo', '-i', 'tests/simple.csv')
    out, err = capsys.readouterr()
    expect = u"xyz | 123\n"
    assert out == expect

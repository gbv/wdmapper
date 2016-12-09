import pytest
import io
import sys
import os

from wdmapper import run


def test_help_as_default(capsys):
    with pytest.raises(SystemExit):
        run()
    out, err = capsys.readouterr()
    assert out.startswith('usage: ')


def test_read_csv(capsys):
    input = io.StringIO(u"foo,bar\n")
    sys.stdin = input
    run('-n', '-H')
    out, err = capsys.readouterr()
    expect = u"foo, bar\n"
    assert out == expect

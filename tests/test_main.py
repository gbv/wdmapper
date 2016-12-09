import pytest

from wdmapper import run


def test_help_as_default(capsys):
    with pytest.raises(SystemExit):
        run()
    out, err = capsys.readouterr()
    assert out.startswith('usage: ')

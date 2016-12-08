import pytest
from wdmapper import main

def test_default(capsys):
    with pytest.raises(SystemExit):
        main()
    out, err = capsys.readouterr()
    assert out.startswith("usage: ")

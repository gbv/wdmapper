import pytest

from wdmapper import run


def test_info(capsys):
    run('P214')
    out, err = capsys.readouterr()
    assert out.startswith("""\
VIAF ID (P214)
<http://www.wikidata.org/entity/P214>
https://viaf.org/viaf/$1
[1-9]""")

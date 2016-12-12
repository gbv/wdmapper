import pytest

from wdmapper.sparql import sparql_query


def test_sparql():
    # just test whether function is defined
    assert sparql_query is not None

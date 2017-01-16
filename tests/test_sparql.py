import pytest

from wdmapper.sparql import SparqlEndpoint


def test_sparql():
    # just test whether class is defined
    assert SparqlEndpoint is not None

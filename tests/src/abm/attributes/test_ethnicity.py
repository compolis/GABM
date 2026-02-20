"""
Unit tests for ethnicity module.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Third-party imports
import pytest
# Local imports
from gabm.abm.attributes.ethnicity import EthnicityID, Ethnicity, EthnicityMap

def test_ethnicity_id_equality_and_hash():
    eid1 = EthnicityID(1)
    eid2 = EthnicityID(1)
    eid3 = EthnicityID(2)
    assert eid1 == eid2
    assert eid1 != eid3
    assert hash(eid1) == hash(eid2)
    assert hash(eid1) != hash(eid3)
    assert str(eid1) == "EthnicityID(1)"


def test_ethnicity():
    eid = EthnicityID(0)
    eth = Ethnicity(eid, 0, "white")
    assert eth.id == eid
    assert eth.value == 0
    assert eth.description == "white"
    assert str(eth) == "white"
    assert repr(eth) == "white"


def test_ethnicity_map():
    emap = EthnicityMap()
    assert isinstance(emap.ethnicity_map, dict)
    # Check default keys and values
    expected = {
        0: "white",
        1: "asian",
        2: "black",
        3: "mixed",
        4: "other"
    }
    for k, v in expected.items():
        eid = EthnicityID(k)
        assert eid in emap.ethnicity_map
        eth = emap.ethnicity_map[eid]
        assert eth.value == k
        assert eth.description == v
    assert "Ethnicities" in str(emap)
    assert "Ethnicities" in repr(emap)

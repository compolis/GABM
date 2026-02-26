"""
Tests for ethnicity module.
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
    description = "unknown"
    eth = Ethnicity(eid, description)
    assert eth.id == eid
    assert eth.description == "unknown"
    assert str(eth) == "unknown"
    assert repr(eth) == "Ethnicity(unknown)"


def test_ethnicity_map():
    emap = EthnicityMap()
    assert isinstance(emap.items, dict[EthnicityID, Ethnicity])
    # Check default keys and values
    expected = {
        0: "unknown",
        1: "white",
        2: "asian",
        3: "black",
        4: "mixed",
        5: "other"
    }
    for k, v in expected.items():
        eid = EthnicityID(k)
        assert eid in emap.items
        eth = emap.items[eid]
        assert eth.id == eid
        assert eth.description == v
    assert "Ethnicities" in str(emap)
    assert "Ethnicities" in repr(emap)

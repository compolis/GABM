"""
Tests for gender module.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.2.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Third-party imports
import pytest
# Local imports
from gabm.abm.attributes.gender import GenderID, Gender, GenderMap
from gabm.abm.attributes.ethnicity import EthnicityID
from gabm.core.id import GABMID

def test_gender_id():
    gid0 = GenderID(0)
    gid1 = GenderID(1)
    gid00 = GenderID(0)
    eid0 = EthnicityID(0)
    gabmid0 = GABMID(0)
    assert str(gid0) == "GenderID(0)"
    assert str(gid1) == "GenderID(1)"
    assert gid0 == gid00
    assert gid0 != gid1
    assert gid0 != eid0
    assert gid0 != gabmid0

def test_gender():
    gid = GenderID(0)
    description = "unknown"
    gender = Gender(gid, description)
    assert gender.id == gid
    assert gender.description == description
    assert str(gender) == f"Gender(id={gid}, description='{description}')"
    assert repr(gender) == f"Gender(id={gid}, description='{description}')"

def test_gender_map_lookup():
    gmap = GenderMap()
    assert isinstance(gmap._map, dict)
    gid0 = GenderID(0)
    gid1 = GenderID(1)
    gid2 = GenderID(2)
    gid3 = GenderID(3)
    expected = {
        gid0: Gender(gid0, "unknown"),
        gid1: Gender(gid1, "female"),
        gid2: Gender(gid2, "male"),
        gid3: Gender(gid3, "non-binary")
    }
    for k, v in expected.items():
        assert k in gmap._map
        gender = gmap._map[k]
        assert gender.id == k
        assert gender.description == v.description
    assert "GenderMap" in str(gmap)
    assert "GenderMap" in repr(gmap)

def test_gender_map_add():
    gmap = GenderMap()
    gid_other = GenderID(99)
    gmap._map[gid_other] = Gender(gid_other, "other")
    assert gmap._map[gid_other].description == "other"

if __name__ == "__main__":
    pytest.main([__file__])

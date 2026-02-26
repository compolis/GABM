"""
Tests for gender module.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Third-party imports
import pytest
# Local imports
from gabm.abm.attributes.gender import GenderID, Gender, GenderMap


def test_gender_id():
    gid1 = GenderID(0)
    gid2 = GenderID(1)
    assert str(gid1) == "GenderID(0)"
    assert gid1 != gid2

def test_gender():
    gid = GenderID(0)
    description = "unknown"
    gender = Gender(gid, description)
    assert gender.id == gid
    assert gender.description == description
    assert str(gender) == description

def test_gender_map_lookup():
    gmap = GenderMap()
    assert gmap.items[GenderID(0)].description == "unknown"
    assert gmap.items[GenderID(1)].description == "female"
    assert gmap.items[GenderID(2)].description == "male"

def test_gender_map_add():
    gmap = GenderMap()
    gid_other = GenderID(99)
    gmap.items[gid_other] = Gender(gid_other, "other")
    assert gmap.items[gid_other].description == "other"

if __name__ == "__main__":
    pytest.main([__file__])

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
    gender = Gender(gid, 0, "female")
    assert gender.id == gid
    assert gender.value == 0
    assert gender.description == "female"
    assert str(gender) == "female"

def test_gender_map_lookup():
    gmap = GenderMap()
    gid_female = GenderID(0)
    gid_male = GenderID(1)
    assert gmap.gender_map[gid_female].description == "female"
    assert gmap.gender_map[gid_male].description == "male"

def test_gender_map_add():
    gmap = GenderMap()
    gid_other = GenderID(99)
    gmap.gender_map[gid_other] = Gender(gid_other, 99, "other")
    assert gmap.gender_map[gid_other].description == "other"

if __name__ == "__main__":
    pytest.main([__file__])

"""
Tests for region module.
"""
# Metadata
__author__ = ["GitHub Copilot <copilot@github.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Local imports
from gabm.abm.attributes.region import RegionID, Region, RegionMap
from gabm.abm.attributes.gender import GenderID
from gabm.core.id import GABMID


def test_region_id():
    """
    Test the RegionID class.
    """
    rid0 = RegionID(0)
    rid1 = RegionID(1)
    rid00 = RegionID(0)
    gid0 = GenderID(0)
    gabmid0 = GABMID(0)

    assert str(rid0) == "RegionID(0)"
    assert str(rid1) == "RegionID(1)"
    assert rid0 == rid00
    assert rid0 != rid1
    assert rid0 != gid0
    assert rid0 != gabmid0


def test_region():
    """
    Test the Region class.
    """
    rid = RegionID(0)
    description = "unknown"
    region = Region(rid, description)

    assert region.id == rid
    assert region.description == description
    assert str(region) == f"Region(id={rid}, description='{description}')"
    assert repr(region) == f"Region(id={rid}, description='{description}')"


def test_region_map_lookup():
    """
    Test RegionMap lookup.
    """
    rmap = RegionMap()
    assert isinstance(rmap._map, dict)
    assert len(rmap._map) == 10
    assert str(rmap._map[RegionID(1)]) == "Region(id=RegionID(1), description='north-west')"

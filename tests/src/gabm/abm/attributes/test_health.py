"""
Tests for health module.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Third-party imports
import pytest
# Local imports
from gabm.abm.attributes.health import HealthID, Health, HealthMap
from gabm.core.id import GABMID

def test_health_id():
    hid0 = HealthID(0)
    hid1 = HealthID(1)
    hid00 = HealthID(0)
    gabmid0 = GABMID(0)
    assert str(hid0) == "HealthID(0)"
    assert str(hid1) == "HealthID(1)"
    assert hid0 == hid00
    assert hid0 != hid1
    assert hid0 != gabmid0

def test_health():
    hid = HealthID(0)
    description = "unknown"
    health = Health(hid, description)
    assert health.id == hid
    assert health.description == description
    assert str(health) == f"Health(id={hid}, description='{description}')"
    assert repr(health) == f"Health(id={hid}, description='{description}')"

def test_health_map_lookup():
    hmap = HealthMap()
    assert isinstance(hmap._map, dict)
    assert len(hmap._map) == 6
    assert str(hmap._map[HealthID(1)]) == "Health(id=HealthID(1), description='very good')"

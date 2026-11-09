"""
Tests for wealth module.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.2.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Third-party imports
import pytest
# Local imports
from gabm.abm.attributes.wealth import WealthID, Wealth
from gabm.abm.attributes.gender import GenderID
from gabm.core.id import GABMID

def test_wealth_id():
    """
    Test the WealthID class.
    """
    wid0 = WealthID(0)
    wid1 = WealthID(1)
    wid00 = WealthID(0)
    gid0 = GenderID(0)
    gabmid0 = GABMID(0)
    assert str(wid0) == "WealthID(0)"
    assert str(wid1) == "WealthID(1)"
    assert wid0 == wid00
    assert wid0 != wid1
    assert wid0 != gid0
    assert wid0 != gabmid0

def test_wealth():
    """
    Test the Wealth class.
    """
    wid = WealthID(0)
    description = "unknown"
    wealth = Wealth(wid, description)
    assert wealth.id == wid
    assert wealth.description == description
    assert str(wealth) == f"Wealth(id={wid}, description='{description}')"
    assert repr(wealth) == f"Wealth(id={wid}, description='{description}')"

def test_wealth_map_lookup():
    """
    Test WealthMap lookup.
    """
    from gabm.abm.attributes.wealth import WealthMap
    wmap = WealthMap()
    assert isinstance(wmap.wealth_map, dict)
    assert len(wmap.wealth_map) == 11
    assert str(wmap.wealth_map[WealthID(1)]) == "Wealth(id=WealthID(1), description='negative')"

"""
Tests for wealth module.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Third-party imports
import pytest
# Local imports
from gabm.abm.attributes.wealth import WealthID, Wealth
from gabm.abm.attributes.ethnicity import EthnicityID
from gabm.core.id import GABMID

def test_wealth_id():
    wid0 = WealthID(0)
    wid1 = WealthID(1)
    wid00 = WealthID(0)
    eid0 = EthnicityID(0)
    gid0 = GABMID(0)
    assert str(wid0) == "WealthID(0)"
    assert str(wid1) == "WealthID(1)"
    assert wid0 == wid00
    assert wid0 != wid1
    assert wid0 != eid0
    assert wid0 != gid0

def test_wealth():
    wid = WealthID(0)
    description = "unknown"
    wealth = Wealth(wid, description)
    assert wealth.id == wid
    assert wealth.description == description
    assert str(wealth) == f"Wealth(id={wid}, description='{description}')"
    assert repr(wealth) == f"Wealth(id={wid}, description='{description}')"

def test_wealth_map_lookup():
    from gabm.abm.attributes.wealth import WealthMap
    wmap = WealthMap()
    assert isinstance(wmap.wealth_map, dict)
    assert len(wmap.wealth_map) == 11
    assert str(wmap.wealth_map[WealthID(1)]) == "Wealth(id=WealthID(1), description='negative')"

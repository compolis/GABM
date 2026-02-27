"""
Tests for income module.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Third-party imports
import pytest
# Local imports
from gabm.abm.attributes.income import IncomeID, Income, IncomeMap
from gabm.abm.attributes.ethnicity import EthnicityID
from gabm.core.id import GABMID

def test_income_id():
    iid0 = IncomeID(0)
    iid1 = IncomeID(1)
    iid00 = IncomeID(0)
    eid0 = EthnicityID(0)
    gid0 = GABMID(0)
    assert str(iid0) == "IncomeID(0)"
    assert str(iid1) == "IncomeID(1)"
    assert iid0 == iid00
    assert iid0 != iid1
    assert iid0 != eid0
    assert iid0 != gid0

def test_income():
    iid = IncomeID(0)
    description = "unknown"
    income = Income(iid, description)
    assert income.id == iid
    assert income.description == description
    assert str(income) == f"Income(id={iid}, description='{description}')"
    assert repr(income) == f"Income(id={iid}, description='{description}')"

def test_income_map_lookup():
    imap = IncomeMap()
    assert isinstance(imap._map, dict)
    assert len(imap._map) == 10
    assert str(imap._map[IncomeID(1)]) == "Income(id=IncomeID(1), description='zero to q1')"

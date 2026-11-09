"""
Tests for employment module.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Local imports
from gabm.abm.attributes.employment import EmploymentID, Employment, EmploymentMap
from gabm.abm.attributes.gender import GenderID
from gabm.core.id import GABMID


def test_employment_id():
    """
    Test the EmploymentID class.
    """
    eid0 = EmploymentID(0)
    eid1 = EmploymentID(1)
    eid00 = EmploymentID(0)
    gid0 = GenderID(0)
    gabmid0 = GABMID(0)

    assert str(eid0) == "EmploymentID(0)"
    assert str(eid1) == "EmploymentID(1)"
    assert eid0 == eid00
    assert eid0 != eid1
    assert eid0 != gid0
    assert eid0 != gabmid0


def test_employment():
    """
    Test the Employment class.
    """
    eid = EmploymentID(0)
    description = "unknown"
    employment = Employment(eid, description)

    assert employment.id == eid
    assert employment.description == description
    assert str(employment) == f"Employment(id={eid}, description='{description}')"
    assert repr(employment) == f"Employment(id={eid}, description='{description}')"


def test_employment_map_lookup():
    """
    Test the EmploymentMap class.
    """
    emap = EmploymentMap()
    assert isinstance(emap._map, dict)
    assert len(emap._map) == 7
    assert str(emap._map[EmploymentID(1)]) == "Employment(id=EmploymentID(1), description='employed full time')"

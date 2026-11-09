"""
Tests for education module.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Local imports
from gabm.abm.attributes.education import EducationID, Education, EducationMap
from gabm.abm.attributes.gender import GenderID
from gabm.core.id import GABMID


def test_education_id():
    """
    Test the EducationID class.
    """
    eid0 = EducationID(0)
    eid1 = EducationID(1)
    eid00 = EducationID(0)
    gid0 = GenderID(0)
    gabmid0 = GABMID(0)

    assert str(eid0) == "EducationID(0)"
    assert str(eid1) == "EducationID(1)"
    assert eid0 == eid00
    assert eid0 != eid1
    assert eid0 != gid0
    assert eid0 != gabmid0


def test_education():
    """
    Test the Education class.
    """
    eid = EducationID(0)
    description = "unknown"
    education = Education(eid, description)

    assert education.id == eid
    assert education.description == description
    assert str(education) == f"Education(id={eid}, description='{description}')"
    assert repr(education) == f"Education(id={eid}, description='{description}')"


def test_education_map_lookup():
    """
    Test the EducationMap class.
    """
    emap = EducationMap()
    assert isinstance(emap._map, dict)
    assert len(emap._map) == 6
    assert str(emap._map[EducationID(1)]) == "Education(id=EducationID(1), description='primary')"

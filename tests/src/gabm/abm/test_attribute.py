"""
Tests for generic attribute base classes.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

import pytest

from gabm.abm.attribute import GABMAttributeID, GABMAttribute, GABMAttributeMap


class DemoAttributeID(GABMAttributeID):
    """Concrete attribute ID for tests."""


class DemoAttribute(GABMAttribute):
    """Concrete attribute for tests."""


def test_attribute_map_basic_access_and_iteration():
    """
    Test basic access and iteration of GABMAttributeMap.
    """
    did = DemoAttributeID(1)
    dattr = DemoAttribute(did, "demo")
    amap = GABMAttributeMap({did: dattr})

    assert len(amap) == 1
    assert did in amap
    assert amap[did] == dattr
    assert amap.get(did) == dattr
    assert list(amap.keys()) == [did]
    assert list(amap.values()) == [dattr]
    assert list(amap.items()) == [(did, dattr)]
    assert list(amap) == [dattr]


def test_attribute_map_type_checks_for_lookup_and_add():
    """
    Test that GABMAttributeMap raises TypeError for invalid types in lookup and add operations.
    """
    did = DemoAttributeID(1)
    dattr = DemoAttribute(did, "demo")
    amap = GABMAttributeMap({did: dattr})

    with pytest.raises(TypeError):
        _ = amap[1]

    with pytest.raises(TypeError):
        _ = amap.get(1)

    with pytest.raises(TypeError):
        amap.add("not-an-attribute")

    class BadAttr:
        def __init__(self):
            self.id = 1

    with pytest.raises(TypeError):
        amap.add(BadAttr())


def test_attribute_map_add_valid_attribute():
    """
    Test adding a valid attribute to the GABMAttributeMap.
    """
    did1 = DemoAttributeID(1)
    did2 = DemoAttributeID(2)
    dattr1 = DemoAttribute(did1, "one")
    dattr2 = DemoAttribute(did2, "two")
    amap = GABMAttributeMap({did1: dattr1})

    amap.add(dattr2)
    assert len(amap) == 2
    assert amap[did2] == dattr2

"""
Tests for core ID module.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

from gabm.core.id import GABMID


class DemoID(GABMID):
    """Concrete ID type for testing equality semantics."""


def test_gabmid_str_repr_and_hash():
    """
    Test that GABMID objects have the correct string representation and hash.
    """
    did = DemoID(7)
    assert str(did) == "DemoID(7)"
    assert repr(did) == "DemoID(7)"
    assert hash(did) == hash(7)


def test_gabmid_equality_requires_same_class_and_value():
    """
    Test that GABMID equality requires both the same class and the same value.
    """
    d1 = DemoID(3)
    d2 = DemoID(3)
    d3 = DemoID(4)
    g1 = GABMID(3)

    assert d1 == d2
    assert d1 != d3
    assert d1 != g1

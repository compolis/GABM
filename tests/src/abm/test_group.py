"""
Tests for the group module.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Standard library imports
import pytest
from gabm.abm.group import GroupID, Group, OpinionatedGroup
from unittest.mock import Mock

# --- GroupID Tests ---
def test_group_id_str_and_repr():
    gid = GroupID(101)
    assert str(gid) == "GroupID(101)"
    assert repr(gid) == "GroupID(101)"

# --- Group Tests ---
def test_group_creation_and_membership():
    gid = GroupID(1)
    group = Group(gid, name="TestGroup")
    assert group.id == gid
    assert group.name == "TestGroup"
    assert isinstance(group.members, set)
    # Add member
    agent = Mock()
    agent.groups = set()
    group.add_member(agent)
    assert agent in group.members
    assert group in agent.groups
    # Remove member
    group.remove_member(agent)
    assert agent not in group.members
    assert group not in agent.groups

def test_group_str_repr_and_list_members():
    group = Group(GroupID(2), name="Alpha")
    s = str(group)
    r = repr(group)
    assert "Group" in s and "members" in s
    assert s == r
    assert isinstance(group.list_members(), tuple)

# --- OpinionatedGroup Tests ---
def test_opinionated_group_creation_and_opinions():
    gid = GroupID(3)
    opinions = {"topic1": Mock(value=5), "topic2": Mock(value=10)}
    ogroup = OpinionatedGroup(gid, name="OpinionGroup", opinions=opinions)
    assert ogroup.opinions == opinions
    assert "opinions" in str(ogroup)
    assert "opinions" in repr(ogroup)

# --- get_AverageOpinion Test ---
def test_opinionated_group_get_average_opinion():
    gid = GroupID(4)
    ogroup = OpinionatedGroup(gid, name="OpinionGroup")
    # Mock members with get_opinion
    member1 = Mock()
    member1.get_opinion = Mock(return_value=Mock(value=2))
    member2 = Mock()
    member2.get_opinion = Mock(return_value=Mock(value=4))
    member3 = Mock()
    member3.get_opinion = Mock(return_value=None)  # No opinion
    ogroup.members = {member1, member2, member3}
    avg = ogroup.get_AverageOpinion("topic")
    assert avg == 3.0
    # No valid opinions
    ogroup.members = set()
    assert ogroup.get_AverageOpinion("topic") is None

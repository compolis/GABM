"""
Tests for the environment module.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Standard library imports
import pytest
# Local imports
from gabm.abm.environment import Environment, OpinionatedEnvironment, Nation
from gabm.abm.agent import AgentID, Agent
from gabm.abm.group import GroupID, Group
from gabm.abm.attributes.opinion import OpinionTopicID, OpinionValue, OpinionValueMap, Opinion

def test_environment_creation_and_str():
    env = Environment(year=2025, place="Mars")
    assert env.year == 2025
    assert env.place == "Mars"
    assert isinstance(env.agents_active, dict)
    assert isinstance(env.groups_active, dict)
    s = str(env)
    r = repr(env)
    assert "Environment" in s
    assert s == r

def test_environment_add_agent_and_group():
    env = Environment()
    agent = Agent(AgentID(1), env)
    group = Group(GroupID(1), name="TestGroup")
    env.agents_active[1] = agent
    env.groups_active[1] = group
    assert env.agents_active[1] == agent
    assert env.groups_active[1] == group

def test_opinionated_environment_creation():
    tid = OpinionTopicID(0)
    val = OpinionValue(tid, 1, "Agree")
    values = OpinionValueMap({tid: val})
    opinion = Opinion(tid, values, 1)
    opinions = {tid: opinion}
    oenv = OpinionatedEnvironment(year=2024, place="Venus", opinions=opinions)
    assert oenv.year == 2024
    assert oenv.place == "Venus"
    assert oenv.opinions[tid] == opinion
    s = str(oenv)
    r = repr(oenv)
    assert "OpinionatedEnvironment" in s
    assert s == r

def test_nation_creation_and_str():
    tid = OpinionTopicID(1)
    val = OpinionValue(tid, 2, "Strongly Agree")
    values = OpinionValueMap({tid: val})
    opinion = Opinion(tid, values, 2)
    opinions = {tid: opinion}
    nation = Nation(year=2023, place="Earth", opinions=opinions, nation="Testland")
    assert nation.nation == "Testland"
    assert nation.opinions[tid] == opinion
    s = str(nation)
    r = repr(nation)
    assert "Nation" in s
    assert s == r

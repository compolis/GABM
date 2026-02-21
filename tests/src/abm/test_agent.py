"""
Tests for the agent module.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Standard library imports
import pytest
from unittest.mock import Mock
# Local imports
from gabm.abm.agent import AgentID, Agent, Animal, Person, Citizen, Alien

# --- AgentID Tests ---
def test_agent_id_str_and_repr():
    aid = AgentID(42)
    assert str(aid) == "AgentID(42)"
    assert repr(aid) == "AgentID(42)"

# --- Agent Tests ---
def test_agent_creation_and_group_membership():
    env = Mock()
    agent = Agent(AgentID(1), env)
    assert agent.id.id == 1
    assert agent.environment == env
    assert isinstance(agent.groups, set)
    # Test join/leave group
    group = Mock()
    agent.join_group(group)
    group.add_member.assert_called_with(agent)
    agent.leave_group(group)
    group.remove_member.assert_called_with(agent)

def test_agent_str_repr():
    env = Mock()
    agent = Agent(AgentID(2), env)
    s = str(agent)
    r = repr(agent)
    assert "Agent" in s and "groups=" in s
    assert s == r

# --- Animal Tests ---
def test_animal_age_and_gender():
    env = Mock()
    env.year = 2026
    gender_map = {0: "female", 1: "male"}
    animal = Animal(AgentID(3), env, year_of_birth=2000, gender_map=gender_map, gender=0)
    assert animal.get_age() == 26
    assert animal.get_gender() == "female"
    # Test default year_of_birth
    animal2 = Animal(AgentID(4), env, gender_map=gender_map, gender=1)
    assert animal2.get_age() == 18
    assert animal2.get_gender() == "male"

# --- Person Tests ---
def test_person_opinion_handling():
    env = Mock()
    env.year = 2026
    # Minimal mock Opinion and OpinionTopicID
    class DummyOpinion:
        def __init__(self, value):
            self.value = value
            self.opinion_id = "topic1"
            self.opinion_values = None
    opinions = {"topic1": DummyOpinion(5)}
    person = Person(AgentID(5), env, opinions=opinions)
    # Deep copy check
    assert person.opinions["topic1"] is not opinions["topic1"]
    # get_opinion
    assert person.get_opinion("topic1").value == 5
    # add_opinion
    new_op = DummyOpinion(7)
    person.add_opinion(new_op, 7)
    assert person.opinions["topic1"].value == 7
    # set_opinion (should raise for non-existent)
    with pytest.raises(ValueError):
        person.set_opinion("notopic", 1)
    # get_opinion_profile (no opinions)
    person2 = Person(AgentID(6), env)
    assert person2.get_opinion_profile() == "I have no opinions."
    # get_self_description
    desc = person.get_self_description()
    assert "years old" in desc

# --- Citizen/Alien Tests ---
def test_citizen_and_alien_creation():
    env = Mock()
    env.year = 2026
    c = Citizen(AgentID(7), env)
    a = Alien(AgentID(8), env)
    assert isinstance(c, Person)
    assert isinstance(a, Person)

# --- Communication Tests (basic) ---
def test_person_communicate_with_llm():
    env = Mock()
    env.year = 2026
    p = Person(AgentID(9), env)
    resp = p.communicate_with_llm("Hello", model="test-model")
    assert resp["response"].startswith("Echo:")
    assert resp["model"] == "test-model"

if __name__ == "__main__":
    pytest.main([__file__])

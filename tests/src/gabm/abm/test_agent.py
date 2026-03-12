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
from gabm.abm.environment import Environment
from gabm.abm.agent import AgentID, Agent, PersonID, Person, CitizenID, Citizen
from gabm.abm.attributes.gender import GenderID, GenderMap

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

# --- Person Tests ---
def test_person_age_and_gender():
    environment = Environment(2026, place="Earth", gender_map=GenderMap())    
    person = Person(PersonID(3), environment=environment, year_of_birth=2000, gender_id=GenderID.FEMALE)
    assert person.get_age() == 26
    assert person.get_gender() == "female"
    # Test default year_of_birth
    person2 = Person(PersonID(4), environment=environment, gender_id=GenderID.MALE)
    assert person2.get_age() == 18
    assert person2.get_gender() == "male"
    # Minimal mock Opinion and OpinionTopicID
    class DummyOpinion:
        def __init__(self, value):
            self.value = value
            self.opinion_id = "topic1"
            self.opinion_values = None
    opinions = {"topic1": DummyOpinion(5)}
    person = Person(PersonID(5), environment=environment, opinions=opinions)
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
    person2 = Person(PersonID(6), environment=environment)
    assert person2.get_opinion_profile() == "I have no opinions."
    # get_self_description
    desc = person.get_self_description()
    assert "years old" in desc

# --- Citizen Tests ---
def test_citizen_creation():
    environment = Environment(2026, place="Earth", gender_map=GenderMap())
    c = Citizen(CitizenID(7), environment=environment)
    assert isinstance(c, Person)

# --- Communication Tests (basic) ---
def test_person_communicate_with_llm():
    environment = Environment(2026, place="Earth", gender_map=GenderMap())
    p = Person(PersonID(9), environment=environment)
    resp = p.communicate_with_llm("Hello", model="test-model")
    assert resp["response"].startswith("Echo:")
    assert resp["model"] == "test-model"

if __name__ == "__main__":
    pytest.main([__file__])

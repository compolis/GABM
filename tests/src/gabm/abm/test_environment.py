"""
Tests for the environment module.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Standard library imports
import pytest
from datetime import date
# Local imports
from gabm.abm.environment import Environment, Nation
from gabm.abm.agent import AgentID, Agent, Person
from gabm.abm.group import GroupID, Group
from gabm.abm.attributes.opinion import OpinionTopicID, OpinionValue, OpinionValueMap, Opinion
from gabm.abm.attributes.interest import InterestTopicID, InterestValue, InterestValueMap, Interest
from gabm.abm.attributes.trait import TraitTopicID, TraitValue, TraitValueMap, Trait

def test_environment_add_agent_and_group():
    """
    Test adding an agent and a group to the Environment.
    """
    env = Environment(year=2026)
    agent = Agent(AgentID(1), env)
    group = Group(GroupID(1), name="TestGroup")
    env.agents_active[1] = agent
    env.groups_active[1] = group
    assert env.agents_active[1] == agent
    assert env.groups_active[1] == group

def test_environment_creation_and_opinions():
    """
    Test the creation of an Environment and its opinions.
    """
    tid = OpinionTopicID(0)
    val = OpinionValue(tid, 1, "Agree")
    values = OpinionValueMap({tid: val})
    opinion = Opinion(tid, values, 1)
    opinions = {tid: opinion}
    oenv = Environment(year=2024, opinions=opinions)
    assert oenv.year == 2024
    assert oenv.name == "Earth"
    assert oenv.opinions[tid] == opinion
    s = str(oenv)
    r = repr(oenv)
    assert "Environment" in s
    assert s == r

def test_nation_creation_and_str():
    """
    Test the creation of a Nation and its string representation.
    """
    tid = OpinionTopicID(1)
    val = OpinionValue(tid, 2, "Strongly Agree")
    values = OpinionValueMap({tid: val})
    opinion = Opinion(tid, values, 2)
    opinions = {tid: opinion}
    nation = Nation(year=2023, name="UK", opinions=opinions)
    assert nation.opinions[tid] == opinion
    s = str(nation)
    r = repr(nation)
    assert "Nation" in s
    assert s == r


def _person_signature(person: Person):
    trait_sig = sorted((topic_id.id, trait.value) for topic_id, trait in person.base_traits.items())
    interest_sig = sorted((topic_id.id, interest.value) for topic_id, interest in person.interests.items())
    return (person.id.id, person.year_of_birth, person.get_gender(), trait_sig, interest_sig)


def test_environment_create_random_people_reproducible():
    """Test bulk random person creation is deterministic when seeded."""
    env_a = Environment(year=2026)
    env_b = Environment(year=2026)

    people_a = env_a.create_random_people(count=4, seed=2026, with_interests=True)
    people_b = env_b.create_random_people(count=4, seed=2026, with_interests=True)

    sig_a = [_person_signature(person) for person in people_a]
    sig_b = [_person_signature(person) for person in people_b]

    assert sig_a == sig_b


def test_environment_create_random_people_registers_agents():
    """Test created people are returned and registered in active agents."""
    env = Environment(year=2026)
    people = env.create_random_people(count=3, start_person_id=100, seed=7, with_interests=False)

    assert len(people) == 3
    assert len(env.agents_active) == 3
    assert all(isinstance(person, Person) for person in people)
    assert [person.id.id for person in people] == [100, 101, 102]
    assert all(len(person.interests) == 0 for person in people)


def test_environment_create_random_people_with_age_range():
    """Random person creation should support explicit sampled age ranges."""
    env = Environment(year=2026)

    people = env.create_random_people(
        count=5,
        start_person_id=1,
        seed=17,
        with_interests=False,
        age_min=20,
        age_max=24,
    )

    assert len(people) == 5
    for person in people:
        assert 20 <= person.get_age() <= 24
        assert person.age_min == person.get_age()
        assert person.age_max == person.get_age()


def test_environment_current_date_defaults_to_start_of_year():
    """Environment should initialize a calendar date for sub-year simulations."""
    env = Environment(year=2026)

    assert env.current_date == date(2026, 1, 1)
    assert env.year == 2026


def test_environment_advance_day_emits_birthday_events():
    """Daily stepping should detect birthdays and support callback hooks."""
    env = Environment(year=2026, current_date=date(2026, 11, 2))
    person = Person(person_id=1, environment=env, year_of_birth=None, gender_id=None, date_of_birth=date(1992, 11, 3))
    env.agents_active[person.id] = person

    callback_events = []

    def on_birthday(p, d):
        callback_events.append((p.id.id, d.isoformat()))

    events = env.advance_day(days=2, birthday_callback=on_birthday)

    assert env.current_date == date(2026, 11, 4)
    assert env.year == 2026
    assert len(events) == 1
    assert events[0][0] == person
    assert events[0][1] == date(2026, 11, 3)
    assert callback_events == [(1, "2026-11-03")]

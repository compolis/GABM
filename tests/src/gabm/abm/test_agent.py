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
from pathlib import Path
# Local imports
from gabm.abm.environment import Environment, Nation
from gabm.abm.agent import AgentID, Agent, PersonID, Person, CitizenID, Citizen
from gabm.abm.attributes.gender import GenderID, GenderMap

# --- AgentID Tests ---
def test_agent_id_str_and_repr():
    """
    Test the string representation and repr of AgentID.
    """
    aid = AgentID(42)
    assert str(aid) == "AgentID(42)"
    assert repr(aid) == "AgentID(42)"

# --- Agent Tests ---
def test_agent_creation_and_group_membership():
    """
    Test the creation of an Agent and its group membership methods.
    """
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
    """
    Test the string representation and repr of Agent.
    """
    env = Mock()
    agent = Agent(AgentID(2), env)
    s = str(agent)
    r = repr(agent)
    assert "Agent" in s and "groups=" in s
    assert s == r

# --- Person Tests ---
def test_person_age_and_gender():
    """
    Test the age and gender methods of Person.
    """
    environment = Environment(2026, name="Earth", gender_map=GenderMap())    
    person = Person(PersonID(3), environment=environment, year_of_birth=2000, gender_id=GenderID.FEMALE)
    assert person.get_age() == 26
    assert person.get_gender() == "female"
    # Test default year_of_birth
    person2 = Person(PersonID(4), environment=environment, year_of_birth=None, gender_id=GenderID.MALE)
    assert person2.get_age() == 18
    assert person2.get_gender() == "male"
    # Minimal mock Opinion and OpinionTopicID
    class DummyOpinion:
        def __init__(self, value):
            self.value = value
            self.opinion_id = "topic1"
            self.opinion_values = None
    opinions = {"topic1": DummyOpinion(5)}
    person = Person(PersonID(5), environment=environment, year_of_birth=None, gender_id=None, opinions=opinions)
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
    person2 = Person(PersonID(6), environment=environment, year_of_birth=None, gender_id=None)
    assert person2.get_opinion_profile() == "I have no opinions."
    # get_self_description
    desc = person.get_self_description()
    assert "years old" in desc


def test_person_age_range_initialization_and_midpoint_age():
    """Age range input should infer a deterministic midpoint age and birth year."""
    environment = Environment(2026, name="Earth", gender_map=GenderMap())

    person = Person(
        PersonID(50),
        environment=environment,
        year_of_birth=None,
        gender_id=GenderID.FEMALE,
        age_min=30,
        age_max=34,
    )

    assert person.age_min == 30
    assert person.age_max == 34
    assert person.get_age() == 32
    assert person.year_of_birth == 1994


def test_person_explicit_age_sets_birth_year_and_bounds():
    """Exact age input should set year_of_birth and age bounds consistently."""
    environment = Environment(2026, name="Earth", gender_map=GenderMap())

    person = Person(
        PersonID(51),
        environment=environment,
        year_of_birth=None,
        gender_id=GenderID.MALE,
        age=40,
    )

    assert person.get_age() == 40
    assert person.year_of_birth == 1986
    assert person.age_min == 40
    assert person.age_max == 40


def test_person_date_of_birth_sets_age_and_year():
    """date_of_birth should populate year_of_birth and age information."""
    from datetime import date

    environment = Environment(2026, name="Earth", gender_map=GenderMap())
    person = Person(
        PersonID(52),
        environment=environment,
        year_of_birth=None,
        gender_id=GenderID.FEMALE,
        date_of_birth=date(2000, 5, 20),
    )

    assert person.year_of_birth == 2000
    assert person.get_age() == 26
    assert person.age_min == 26
    assert person.age_max == 26


def test_person_rejects_invalid_age_inputs():
    """Invalid age combinations should raise ValueError."""
    environment = Environment(2026, name="Earth", gender_map=GenderMap())

    with pytest.raises(ValueError):
        Person(PersonID(53), environment=environment, year_of_birth=None, gender_id=None, age=-1)

    with pytest.raises(ValueError):
        Person(PersonID(54), environment=environment, year_of_birth=None, gender_id=None, age_min=40, age_max=30)

    with pytest.raises(ValueError):
        Person(
            PersonID(55),
            environment=environment,
            year_of_birth=1990,
            gender_id=None,
            age=20,
        )


def test_person_age_helpers_for_exact_age():
    """Exact-age person should report exact age semantics and no birthday tuple."""
    environment = Environment(2026, name="Earth", gender_map=GenderMap())
    person = Person(
        PersonID(56),
        environment=environment,
        year_of_birth=None,
        gender_id=GenderID.MALE,
        age=27,
    )

    assert person.has_exact_age() is True
    assert person.get_age_range() == (27, 27)
    assert person.get_birthday_month_day() is None


def test_person_age_helpers_for_age_range():
    """Age-range person should report non-exact age semantics."""
    environment = Environment(2026, name="Earth", gender_map=GenderMap())
    person = Person(
        PersonID(57),
        environment=environment,
        year_of_birth=None,
        gender_id=GenderID.FEMALE,
        age_min=18,
        age_max=24,
    )

    assert person.has_exact_age() is False
    assert person.get_age_range() == (18, 24)
    assert person.get_birthday_month_day() is None
    assert "between 18 and 24 years old" in person.get_self_description()


def test_person_age_helpers_for_date_of_birth():
    """date_of_birth person should expose month/day for anniversary simulations."""
    from datetime import date

    environment = Environment(2026, name="Earth", gender_map=GenderMap())
    person = Person(
        PersonID(58),
        environment=environment,
        year_of_birth=None,
        gender_id=GenderID.FEMALE,
        date_of_birth=date(1992, 11, 3),
    )

    assert person.has_exact_age() is True
    assert person.get_age_range() == (34, 34)
    assert person.get_birthday_month_day() == (11, 3)
    assert person.is_birthday(11, 3) is True
    assert person.is_birthday(11, 4) is False


def test_person_is_birthday_without_dob_is_false_and_invalid_date_raises():
    """Birthday helper should be safe without DOB and validate obvious bad input."""
    environment = Environment(2026, name="Earth", gender_map=GenderMap())
    person = Person(
        PersonID(59),
        environment=environment,
        year_of_birth=2000,
        gender_id=GenderID.FEMALE,
    )

    assert person.is_birthday(1, 1) is False

    with pytest.raises(ValueError):
        person.is_birthday(0, 1)

    with pytest.raises(ValueError):
        person.is_birthday(1, 0)


def test_person_name_set_get_with_explicit_name():
    """Test explicit name is preserved and can be updated via setter/getter."""
    environment = Environment(2026, name="Earth", gender_map=GenderMap())
    person = Person(PersonID(10), environment=environment, year_of_birth=1995, gender_id=GenderID.FEMALE, name="Ari")

    assert person.get_name() == "Ari"

    person.set_name("Jordan")
    assert person.get_name() == "Jordan"


def test_person_set_name_rejects_empty_or_none():
    """Test name setter validates empty and None values."""
    environment = Environment(2026, name="Earth", gender_map=GenderMap())
    person = Person(PersonID(11), environment=environment, year_of_birth=1990, gender_id=GenderID.MALE, name="Alex")

    with pytest.raises(ValueError):
        person.set_name("")

    with pytest.raises(ValueError):
        person.set_name(None)


def test_person_auto_assigns_name_from_ons_when_missing(tmp_path):
    """Test automatic name assignment uses ONS files and person demographics."""
    male_csv = tmp_path / "male.csv"
    female_csv = tmp_path / "female.csv"

    male_csv.write_text(
        "Name,Alex,Sam\n"
        "1990,1,2\n"
        "2000,2,1\n",
        encoding="utf-8",
    )
    female_csv.write_text(
        "Name,Ava,Ella\n"
        "1990,2,1\n"
        "2000,1,2\n",
        encoding="utf-8",
    )

    environment = Environment(2026, name="Earth", gender_map=GenderMap())
    person = Person(
        PersonID(12),
        environment=environment,
        year_of_birth=2000,
        gender_id=GenderID.FEMALE,
        name=None,
        ons_male_file=Path(male_csv),
        ons_female_file=Path(female_csv),
    )

    assert person.get_name() in {"Ava", "Ella"}

# --- Citizen Tests ---
def test_citizen_creation():
    """
    Test the creation of a Citizen object and its inheritance from Person.
    """
    environment = Nation(2026, name="Earth", gender_map=GenderMap())
    c = Citizen(CitizenID(7), nation=environment)
    assert isinstance(c, Person)

# --- Communication Tests (basic) ---
def test_person_communicate_with_llm():
    """
    Test the communicate_with_llm method of Person.
    """
    environment = Environment(2026, name="Earth", gender_map=GenderMap())
    p = Person(PersonID(9), environment=environment, year_of_birth=None, gender_id=None)
    resp = p.communicate_with_llm("Hello", model="test-model")
    assert resp["response"].startswith("Echo:")
    assert resp["model"] == "test-model"

if __name__ == "__main__":
    pytest.main([__file__])

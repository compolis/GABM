"""
Tests for Person trait-driven interest generation.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import random
import pytest

# Local imports
from gabm.abm.environment import Environment
from gabm.abm.agent import PersonID, Person
from gabm.abm.attributes.gender import GenderMap
from gabm.abm.attributes.interest import InterestTopicID, InterestTopic, Interest, InterestValue, InterestValueMap
from gabm.abm.attributes.trait import TraitTopicID, TraitValue, TraitValueMap, Trait
from gabm.abm.attributes.values import ValueTopicID, ValueStrengthMap, Values


def _make_trait(topic_id: int, value: int, description: str) -> Trait:    
    trait_topic_id = TraitTopicID(topic_id)
    trait_value = TraitValue(trait_topic_id, value, description)
    return Trait(trait_topic_id, TraitValueMap({trait_topic_id: trait_value}), value)


def _make_interest(topic_id: int, value: int, description: str) -> Interest:
    interest_topic_id = InterestTopicID(topic_id)
    interest_value = InterestValue(interest_topic_id, value, description)
    return Interest(interest_topic_id, InterestValueMap({interest_topic_id: interest_value}), value)


def _interest_signature(person: Person):
    return sorted((topic_id.id, interest.value) for topic_id, interest in person.interests.items())


def _values_signature(person: Person):
    return sorted((topic_id.id, value.value) for topic_id, value in person.values.items())


def _make_value(topic_id: int, value: int, description: str) -> Values:
    value_topic_id = ValueTopicID(topic_id)
    value_map = ValueStrengthMap.default_for_topic(value_topic_id, value=value, description=description)
    return Values(value_topic_id, value_map, value)


def test_person_traits_are_optional_and_deep_copied():
    """
    Test that Person traits are optional and deep copied.
    """
    environment = Environment(year=2026, name="Earth", gender_map=GenderMap())
    openness = _make_trait(0, 2, "very high")
    traits = {TraitTopicID(0): openness}

    person = Person(person_id=PersonID(10), environment=environment, year_of_birth=None, gender_id=None, traits=traits)

    assert person.get_trait(TraitTopicID(0)) is not None
    assert person.get_trait(TraitTopicID(0)).value == 2
    assert person.get_trait(TraitTopicID(0)) is not openness


def test_generate_interests_from_traits_reproducible_with_global_seed():
    """
    Test that generating interests from traits is reproducible with a global seed.
    """
    environment = Environment(year=2026, name="Earth", gender_map=GenderMap())
    traits = {TraitTopicID(0): _make_trait(0, 2, "very high")}

    person_a = Person(person_id=PersonID(11), environment=environment, year_of_birth=None, gender_id=None, traits=traits)
    person_b = Person(person_id=PersonID(12), environment=environment, year_of_birth=None, gender_id=None, traits=traits)

    seed = 42
    random.seed(seed)
    person_a.generate_interests_from_traits()
    signature_a = _interest_signature(person_a)

    random.seed(seed)
    person_b.generate_interests_from_traits()
    signature_b = _interest_signature(person_b)

    assert signature_a == signature_b


def test_generate_interests_from_traits_openness_affects_interest_count():
    """
    Test that higher openness trait values lead to more generated interests.
    """
    environment = Environment(year=2026, name="Earth", gender_map=GenderMap())
    high_traits = {TraitTopicID(0): _make_trait(0, 2, "very high")}
    low_traits = {TraitTopicID(0): _make_trait(0, -1, "low")}


    person_high = Person(person_id=PersonID(13), environment=environment, year_of_birth=None, gender_id=None, traits=high_traits)
    person_low = Person(person_id=PersonID(14), environment=environment, year_of_birth=None, gender_id=None, traits=low_traits)

    seed = 42
    random.seed(seed)
    person_high.generate_interests_from_traits()
    random.seed(seed)
    person_low.generate_interests_from_traits()

    assert len(person_high.interests) > len(person_low.interests)


def test_generate_interests_from_traits_does_not_overwrite_existing_by_default():
    """
    Test that generating interests from traits does not overwrite existing interests by default.
    """
    environment = Environment(year=2026, name="Earth", gender_map=GenderMap())
    existing = {InterestTopicID(8): _make_interest(8, 1, "interested")}
    traits = {TraitTopicID(0): _make_trait(0, 2, "very high")}

    person = Person(person_id=PersonID(15), environment=environment, year_of_birth=None, gender_id=None, interests=existing, traits=traits)
    person.generate_interests_from_traits(seed=42)

    assert len(person.interests) == 1
    assert InterestTopicID(8) in person.interests


def test_generate_interests_from_traits_reproducible_with_seed_argument():
    """
    Test that generating interests from traits is reproducible with a seed argument.
    """
    environment = Environment(year=2026, name="Earth", gender_map=GenderMap())
    traits = {TraitTopicID(0): _make_trait(0, 1, "high")}

    person_a = Person(person_id=PersonID(16), environment=environment, year_of_birth=None, gender_id=None, traits=traits)
    person_b = Person(person_id=PersonID(17), environment=environment, year_of_birth=None, gender_id=None, traits=traits)

    # Disturb global RNG state to ensure seed argument path is independent.
    seed = 42
    person_a.generate_interests_from_traits(seed=seed)
    signature_a = _interest_signature(person_a)

    person_b.generate_interests_from_traits(seed=seed)
    signature_b = _interest_signature(person_b)

    assert signature_a == signature_b


def test_generate_interests_from_traits_can_use_custom_interest_topics():
    """Test generating interests from a caller-provided topic catalog."""
    environment = Environment(year=2026, name="Earth", gender_map=GenderMap())
    traits = {TraitTopicID(0): _make_trait(0, 1, "high")}
    person = Person(person_id=PersonID(27), environment=environment, year_of_birth=None, gender_id=None, traits=traits)

    custom_topics = {
        InterestTopicID(100): InterestTopic(InterestTopicID(100), "astrophotography", "Capturing night sky images"),
        InterestTopicID(200): InterestTopic(InterestTopicID(200), "urban gardening", "Growing food in city spaces"),
        InterestTopicID(300): InterestTopic(InterestTopicID(300), "podcast editing", "Editing and producing podcasts"),
    }

    seed = 42
    person.generate_interests_from_traits(seed=seed, interest_topics=custom_topics)

    assert len(person.interests) > 0
    assert set(person.interests.keys()).issubset(set(custom_topics.keys()))


def test_generate_default_interests_uses_default_topic_catalog():
    """Test Person convenience wrapper for default trait-guided interest generation."""
    environment = Environment(year=2026, name="Earth", gender_map=GenderMap())
    traits = {TraitTopicID(0): _make_trait(0, 1, "high")}
    person = Person(person_id=PersonID(28), environment=environment, year_of_birth=None, gender_id=None, traits=traits)

    seed = 42
    person.generate_default_interests(seed=seed)

    assert len(person.interests) > 0
    assert all(0 <= topic_id.id <= 8 for topic_id in person.interests.keys())


def test_with_random_traits_reproducible_with_seed():
    """Test Person factory for random traits is deterministic when seeded."""
    environment = Environment(year=2026, name="Earth", gender_map=GenderMap())
    seed = 42
    person_a = Person.with_random_traits(
        person_id=PersonID(29),
        environment=environment,
        year_of_birth=None,
        gender_id=None,
        seed=seed,
    )
    person_b = Person.with_random_traits(
        person_id=PersonID(30),
        environment=environment,
        year_of_birth=None,
        gender_id=None,
        seed=seed,
    )

    traits_a = sorted((topic_id.id, trait.value) for topic_id, trait in person_a.base_traits.items())
    traits_b = sorted((topic_id.id, trait.value) for topic_id, trait in person_b.base_traits.items())

    assert traits_a == traits_b


def test_with_random_traits_can_generate_default_interests():
    """Test Person factory can optionally generate trait-guided default interests."""
    environment = Environment(year=2026, name="Earth", gender_map=GenderMap())
    seed = 42
    intersest_seed = seed + 1
    person = Person.with_random_traits(
        person_id=PersonID(31),
        environment=environment,
        year_of_birth=None,
        gender_id=None,
        seed=seed,
        generate_interests=True,
        interest_seed=intersest_seed,
    )

    assert len(person.interests) > 0
    assert all(0 <= topic_id.id <= 8 for topic_id in person.interests.keys())


def test_get_interests_summary_all_neutral_message():
    """Test summary for all-neutral interests."""
    environment = Environment(year=2026, name="Earth", gender_map=GenderMap())
    person = Person(person_id=PersonID(34), environment=environment, year_of_birth=None, gender_id=None)
    person.interests = {
        InterestTopicID(1): _make_interest(1, 0, "neutral"),
        InterestTopicID(2): _make_interest(2, 0, "neutral"),
    }

    summary = person.get_interests_summary()

    assert summary == "I don't currently have any interests."


def test_get_interests_summary_prioritizes_strongest_like_and_dislike():
    """Test summary highlights strongest interests and disinterests."""
    environment = Environment(year=2026, name="Earth", gender_map=GenderMap())
    person = Person(person_id=PersonID(32), environment=environment, year_of_birth=None, gender_id=None)
    person.interests = {
        InterestTopicID(3): _make_interest(3, 2, "very interested"),
        InterestTopicID(7): _make_interest(7, 2, "very interested"),
        InterestTopicID(4): _make_interest(4, -2, "strongly dislike"),
        InterestTopicID(0): _make_interest(0, -2, "strongly dislike"),
    }

    summary = person.get_interests_summary()

    assert summary == "I am interested in music and reading. I am not interested in science and sport."


def test_get_interests_summary_falls_back_to_interested_and_disliked():
    """Test summary fallback when no very interested/disinterested values exist."""
    environment = Environment(year=2026, name="Earth", gender_map=GenderMap())
    person = Person(person_id=PersonID(33), environment=environment, year_of_birth=None, gender_id=None)
    person.interests = {
        InterestTopicID(3): _make_interest(3, 1, "interested"),
        InterestTopicID(7): _make_interest(7, 1, "interested"),
        InterestTopicID(4): _make_interest(4, -1, "dislike"),
    }

    summary = person.get_interests_summary()

    assert summary == "I am interested in music and reading. I am not interested in sport."


def test_get_interests_summary_only_disinterests():
    """Test summary when only disinterests are present."""
    environment = Environment(year=2026, name="Earth", gender_map=GenderMap())
    person = Person(person_id=PersonID(35), environment=environment, year_of_birth=None, gender_id=None)
    person.interests = {
        InterestTopicID(4): _make_interest(4, -2, "strongly dislike"),
        InterestTopicID(0): _make_interest(0, -1, "dislike"),
        InterestTopicID(1): _make_interest(1, 0, "neutral"),
    }

    summary = person.get_interests_summary()

    assert summary == "I am not interested in sport."


def test_get_interests_summary_only_interests():
    """Test summary when only interests are present."""
    environment = Environment(year=2026, name="Earth", gender_map=GenderMap())
    person = Person(person_id=PersonID(36), environment=environment, year_of_birth=None, gender_id=None)
    person.interests = {
        InterestTopicID(3): _make_interest(3, 1, "interested"),
        InterestTopicID(7): _make_interest(7, 1, "interested"),
        InterestTopicID(2): _make_interest(2, 0, "neutral"),
    }

    summary = person.get_interests_summary()

    assert summary == "I am interested in music and reading."


def test_person_values_auto_generated_by_default():
    """Test that values are generated when none are provided."""
    environment = Environment(year=2026, name="Earth", gender_map=GenderMap())
    person = Person(person_id=PersonID(37), environment=environment, year_of_birth=1996, gender_id=None)

    assert len(person.values) == 10
    assert person.get_value_priority(ValueTopicID(0)) is not None


def test_person_values_can_be_provided_and_deep_copied():
    """Test provided values are deep copied and retained."""
    environment = Environment(year=2026, name="Earth", gender_map=GenderMap())
    provided_values = Values.default_profile(seed=42, stochastic=False)
    person = Person(
        person_id=PersonID(38),
        environment=environment,
        year_of_birth=1990,
        gender_id=None,
        values=provided_values,
    )

    assert _values_signature(person) == sorted((tid.id, v.value) for tid, v in provided_values.items())
    assert person.values[ValueTopicID(0)] is not provided_values[ValueTopicID(0)]


def test_generate_values_profile_reproducible_with_seed():
    """Test regenerating values profile is reproducible with seed."""
    environment = Environment(year=2026, name="Earth", gender_map=GenderMap())
    person_a = Person(person_id=PersonID(39), environment=environment, year_of_birth=1995, gender_id=None)
    person_b = Person(person_id=PersonID(40), environment=environment, year_of_birth=1995, gender_id=None)

    seed = 42
    person_a.generate_values_profile(seed=seed, economic_security="high", stochastic=True, overwrite=True)
    person_b.generate_values_profile(seed=seed, economic_security="high", stochastic=True, overwrite=True)

    assert _values_signature(person_a) == _values_signature(person_b)


def test_get_values_summary_highlights_top_and_low_priorities():
    """Test values summary highlights highest and lowest-priority domains."""
    environment = Environment(year=2026, name="Earth", gender_map=GenderMap())
    person = Person(person_id=PersonID(41), environment=environment, year_of_birth=1990, gender_id=None)
    person.values = {
        ValueTopicID(0): _make_value(0, 5, "core priority"),
        ValueTopicID(1): _make_value(1, 5, "core priority"),
        ValueTopicID(9): _make_value(9, 1, "very low priority"),
    }

    summary = person.get_values_summary()

    assert summary == "I value family and relationships and health and wellbeing."


def test_get_values_summary_balanced_message_for_flat_profile():
    """Test values summary when priorities are equal across domains."""
    environment = Environment(year=2026, name="Earth", gender_map=GenderMap())
    person = Person(person_id=PersonID(42), environment=environment, year_of_birth=1990, gender_id=None)
    person.values = {
        ValueTopicID(0): _make_value(0, 3, "important"),
        ValueTopicID(1): _make_value(1, 3, "important"),
    }

    summary = person.get_values_summary()

    assert summary == ""


def test_get_values_summary_no_profile_message():
    """Test values summary when no values profile exists."""
    environment = Environment(year=2026, name="Earth", gender_map=GenderMap())
    person = Person(person_id=PersonID(43), environment=environment, year_of_birth=1990, gender_id=None)
    person.values = {}

    summary = person.get_values_summary()

    assert summary == ""


def test_person_has_immutable_initial_big_five_values():
    """
    Test that a Person has immutable initial Big Five trait values.
    """
    environment = Environment(year=2026, name="Earth", gender_map=GenderMap())
    person = Person(person_id=PersonID(18), environment=environment, year_of_birth=None, gender_id=None)

    for trait_topic in range(5):
        assert person.get_initial_trait_value(TraitTopicID(trait_topic)) == 0
        assert person.get_trait(TraitTopicID(trait_topic)) is not None

    with pytest.raises(TypeError):
        person.initial_trait_values[TraitTopicID(0)] = 2


def test_base_traits_can_change_without_changing_initial_values():
    """
    Test that changing a Person's base trait values does not change the initial values.
    """
    environment = Environment(year=2026, name="Earth", gender_map=GenderMap())
    traits = {TraitTopicID(0): _make_trait(0, 2, "very high")}
    person = Person(person_id=PersonID(19), environment=environment, year_of_birth=None, gender_id=None, traits=traits)

    assert person.get_initial_trait_value(TraitTopicID(0)) == 2
    person.set_base_trait_value(TraitTopicID(0), -1, "low")

    assert person.get_initial_trait_value(TraitTopicID(0)) == 2
    assert person.get_trait(TraitTopicID(0)).value == -1


def test_self_and_other_trait_opinions_support_higher_order():
    """
    Test that a Person can have self and other trait opinions with higher order values.
    """
    environment = Environment(year=2026, name="Earth", gender_map=GenderMap())
    person = Person(person_id=PersonID(20), environment=environment, year_of_birth=None, gender_id=None)

    openness = TraitTopicID(0)
    person.set_self_trait_opinion(openness, 1)
    assert person.get_self_trait_opinion(openness) == 1

    person.set_other_trait_opinion(other_agent_id=21, trait_id=openness, value=-1, order=1)
    person.set_other_trait_opinion(other_agent_id=21, trait_id=openness, value=2, order=2)

    assert person.get_other_trait_opinion(other_agent_id=21, trait_id=openness, order=1) == -1
    assert person.get_other_trait_opinion(other_agent_id=21, trait_id=openness, order=2) == 2

    with pytest.raises(ValueError):
        person.set_other_trait_opinion(other_agent_id=21, trait_id=openness, value=0, order=0)


def test_trait_state_export_import_roundtrip():
    """
    Test that exporting and importing a Person's trait state preserves the trait values and opinions.
    """
    environment = Environment(year=2026, name="Earth", gender_map=GenderMap())
    source = Person(person_id=PersonID(22), environment=environment, year_of_birth=None, gender_id=None)

    openness = TraitTopicID(0)
    source.set_base_trait_value(openness, 1.5)
    source.set_self_trait_opinion(openness, 2.0)
    source.set_other_trait_opinion(other_agent_id=99, trait_id=openness, value=-0.5, order=2)

    state = source.export_trait_state()

    target = Person(person_id=PersonID(23), environment=environment, year_of_birth=None, gender_id=None)
    target.import_trait_state(state)

    assert target.get_initial_trait_value(openness) == source.get_initial_trait_value(openness)
    assert target.get_trait(openness).value == 1.5
    assert target.get_self_trait_opinion(openness) == 2.0
    assert target.get_other_trait_opinion(other_agent_id=99, trait_id=openness, order=2) == -0.5


def test_reflect_on_traits_moves_towards_self_opinion_reproducibly():
    """
    Test that reflecting on traits moves the base trait values towards the self-opinion values reproducibly.
    """
    environment = Environment(year=2026, name="Earth", gender_map=GenderMap())
    person_a = Person(person_id=PersonID(24), environment=environment, year_of_birth=None, gender_id=None)
    person_b = Person(person_id=PersonID(25), environment=environment, year_of_birth=None, gender_id=None)

    openness = TraitTopicID(0)
    person_a.set_base_trait_value(openness, 0.0)
    person_b.set_base_trait_value(openness, 0.0)

    person_a.set_self_trait_opinion(openness, 2.0)
    person_b.set_self_trait_opinion(openness, 2.0)

    person_a.reflect_on_traits(learning_rate=0.5, seed=123)
    person_b.reflect_on_traits(learning_rate=0.5, seed=123)

    assert person_a.get_trait(openness).value == person_b.get_trait(openness).value
    assert person_a.get_trait(openness).value > 0.0


def test_reflect_on_traits_rejects_negative_learning_rate():
    """
    Test that reflect_on_traits raises a ValueError for negative learning rates.
    """
    environment = Environment(year=2026, name="Earth", gender_map=GenderMap())
    person = Person(person_id=PersonID(26), environment=environment, year_of_birth=None, gender_id=None)

    with pytest.raises(ValueError):
        person.reflect_on_traits(learning_rate=-0.1)

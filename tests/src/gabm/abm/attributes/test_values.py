"""
Tests for values module.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Third-party imports
import pytest

# Local imports
from gabm.abm.attributes.values import (
    ValueTopicID,
    ValueTopic,
    ValueStrength,
    ValueStrengthMap,
    Values,
)
from gabm.abm.attributes.gender import GenderID
from gabm.core.id import GABMID


def test_value_topic_id():
    vtid0 = ValueTopicID(0)
    vtid1 = ValueTopicID(1)
    vtid00 = ValueTopicID(0)
    gid0 = GenderID(0)
    gabmid0 = GABMID(0)

    assert str(vtid0) == "ValueTopicID(0)"
    assert vtid0 == vtid00
    assert vtid0 != vtid1
    assert vtid0 != gid0
    assert vtid0 != gabmid0


def test_value_topic_default_topics():
    topics = ValueTopic.default_topics()

    assert len(topics) == 10
    assert [topic_id.id for topic_id in topics.keys()] == list(range(10))
    assert topics[ValueTopicID(0)].topic == "family and relationships"
    assert topics[ValueTopicID(1)].topic == "health and wellbeing"
    assert topics[ValueTopicID(9)].topic == "status, wealth, and influence"


def test_value_strength_and_map():
    tid = ValueTopicID(0)
    strength = ValueStrength(tid, 4, "core priority")
    value_map = ValueStrengthMap({tid: strength})

    assert strength.value_topic_id == tid
    assert strength.value == 4
    assert strength.description == "core priority"
    assert value_map.values[tid] == strength


def test_values_get_description():
    tid = ValueTopicID(0)
    strength = ValueStrength(tid, 3, "very important")
    value_map = ValueStrengthMap({tid: strength})
    values = Values(tid, value_map, 3)

    assert values.get_description() == "very important"


def test_values_set_value_rejects_invalid_for_map():
    tid = ValueTopicID(0)
    strength = ValueStrength(tid, 3, "very important")
    value_map = ValueStrengthMap({tid: strength})
    values = Values(tid, value_map, 3)

    with pytest.raises(ValueError):
        values.set_value(1)


def test_values_default_profile_reproducible_with_seed():
    profile_a = Values.default_profile(seed=2026)
    profile_b = Values.default_profile(seed=2026)

    sig_a = sorted((topic_id.id, value.value) for topic_id, value in profile_a.items())
    sig_b = sorted((topic_id.id, value.value) for topic_id, value in profile_b.items())

    assert sig_a == sig_b


def test_values_default_profile_age_pattern_without_noise():
    young = Values.default_profile(age=24, stochastic=False)
    old = Values.default_profile(age=70, stochastic=False)

    # Younger adults generally emphasize achievement more than older adults.
    assert young[ValueTopicID(4)].value >= old[ValueTopicID(4)].value
    # Older adults generally emphasize security more than younger adults.
    assert old[ValueTopicID(2)].value >= young[ValueTopicID(2)].value


def test_values_default_profile_economic_security_pattern_without_noise():
    low_security = Values.default_profile(economic_security="low", stochastic=False)
    high_security = Values.default_profile(economic_security="high", stochastic=False)

    # Less secure conditions emphasize security and stability.
    assert low_security[ValueTopicID(2)].value >= high_security[ValueTopicID(2)].value
    # More secure conditions emphasize freedom and independence.
    assert high_security[ValueTopicID(3)].value >= low_security[ValueTopicID(3)].value

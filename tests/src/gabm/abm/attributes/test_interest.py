"""
Tests for interest module.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Third-party imports
import pytest
# Local imports
from gabm.abm.attributes.interest import InterestTopicID, InterestTopic, InterestValue, InterestValueMap, Interest
from gabm.abm.attributes.gender import GenderID
from gabm.core.id import GABMID

def test_interest_topic_id():
    """
    Test the InterestTopicID class.
    """
    itid0 = InterestTopicID(0)
    itid1 = InterestTopicID(1)
    itid00 = InterestTopicID(0)
    gid0 = GenderID(0)
    gabmid0 = GABMID(0)
    assert str(itid0) == "InterestTopicID(0)"
    assert itid0 == itid00
    assert itid0 != itid1
    assert itid0 != gid0
    assert itid0 != gabmid0

def test_interest_topic():
    """
    Test the InterestTopic class.
    """
    tid = InterestTopicID(0)
    topic = InterestTopic(tid, "high", "A high interest.")
    assert topic.id == tid
    assert topic.topic == "high"
    assert topic.description == "A high interest."
    assert "InterestTopic" in str(topic)
    assert "InterestTopic" in repr(topic)


def test_interest_topic_default_topics():
    """Test default interest topic catalog."""
    topics = InterestTopic.default_topics()

    assert len(topics) == 9
    assert [topic_id.id for topic_id in topics.keys()] == list(range(9))
    assert topics[InterestTopicID(0)].topic == "science"
    assert topics[InterestTopicID(8)].topic == "gaming"

def test_interest_value():
    """
    Test the InterestValue class.
    """
    tid = InterestTopicID(0)
    val = InterestValue(tid, 2, "Very high")
    assert val.interest_topic_id == tid
    assert val.value == 2
    assert val.description == "Very high"
    assert "InterestValue" in str(val)
    assert "InterestValue" in repr(val)

def test_interest_value_map():
    """
    Test the InterestValueMap class.
    """
    tid = InterestTopicID(0)
    val = InterestValue(tid, 2, "Very high")
    values = InterestValueMap({tid: val})
    assert values.values[tid] == val
    assert "InterestValueMap" in str(values)


def test_interest_value_map_default_for_topic():
    """Test default map factory for simulation-friendly setup."""
    tid = InterestTopicID(3)
    values = InterestValueMap.default_for_topic(tid)

    assert tid in values.values
    assert values.values[tid].interest_topic_id == tid
    assert values.values[tid].value == 0
    assert values.values[tid].description == "neutral"


def test_interest_value_map_default_for_topics():
    """Test default map factory for multiple topics."""
    topic_ids = [InterestTopicID(1), InterestTopicID(4), InterestTopicID(7)]
    values = InterestValueMap.default_for_topics(topic_ids, value=1, description="interested")

    assert set(values.values.keys()) == set(topic_ids)
    for topic_id in topic_ids:
        assert values.values[topic_id].interest_topic_id == topic_id
        assert values.values[topic_id].value == 1
        assert values.values[topic_id].description == "interested"

def test_interest():
    """
    Test the Interest class.
    """
    tid = InterestTopicID(0)
    val = InterestValue(tid, 2, "Very high")
    values = InterestValueMap({tid: val})
    interest = Interest(tid, values, 2)
    assert interest.id == tid
    assert interest.interest_values == values
    assert interest.value == 2
    assert "Interest" in str(interest)
    assert interest.get_description() == "Very high"
    interest2 = Interest(tid, values, 99)
    assert interest2.get_description() is None

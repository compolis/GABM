"""
Unit tests for opinion module.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Third-party imports
import pytest
# Local imports
from gabm.abm.attributes.opinion import OpinionTopicID, OpinionTopic, OpinionValue, OpinionValueMap, Opinion

def test_opinion_topic_id_equality_and_hash():
    tid1 = OpinionTopicID(1)
    tid2 = OpinionTopicID(1)
    tid3 = OpinionTopicID(2)
    assert tid1 == tid2
    assert tid1 != tid3
    assert hash(tid1) == hash(tid2)
    assert hash(tid1) != hash(tid3)
    assert str(tid1) == "OpinionTopicID(1)"

def test_opinion_topic():
    tid = OpinionTopicID(0)
    topic = OpinionTopic(tid, "positive", "A positive opinion.")
    assert topic.id == tid
    assert topic.topic == "positive"
    assert topic.description == "A positive opinion."
    assert "OpinionTopic" in str(topic)
    assert "OpinionTopic" in repr(topic)

def test_opinion_value():
    tid = OpinionTopicID(0)
    val = OpinionValue(tid, 2, "Strongly positive")
    assert val.opinion_topic_id == tid
    assert val.value == 2
    assert val.description == "Strongly positive"
    assert "OpinionValue" in str(val)
    assert "OpinionValue" in repr(val)

def test_opinion_value_map():
    tid = OpinionTopicID(0)
    val = OpinionValue(tid, 2, "Strongly positive")
    values = OpinionValueMap({tid: val})
    assert values.values[tid] == val
    assert "OpinionValueMap" in str(values)

def test_opinion():
    tid = OpinionTopicID(0)
    val = OpinionValue(tid, 2, "Strongly positive")
    values = OpinionValueMap({tid: val})
    opinion = Opinion(tid, values, 2)
    assert opinion.id == tid
    assert opinion.opinion_values == values
    assert opinion.value == 2
    assert "Opinion" in str(opinion)
    assert opinion.get_description() == "Strongly positive"
    opinion2 = Opinion(tid, values, 99)
    assert opinion2.get_description() is None

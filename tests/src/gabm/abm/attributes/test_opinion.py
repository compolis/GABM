"""
Tests for opinion module.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.2.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Third-party imports
import pytest
# Local imports
from gabm.abm.attributes.opinion import OpinionTopicID, OpinionTopic, OpinionValue, OpinionValueMap, Opinion
from gabm.abm.attributes.gender import GenderID
from gabm.core.id import GABMID

def test_opinion_topic_id():
    """
    Test the OpinionTopicID class.
    """
    otid0 = OpinionTopicID(0)
    otid1 = OpinionTopicID(1)
    otid00 = OpinionTopicID(0)
    gid0 = GenderID(0)
    gabmid0 = GABMID(0)
    assert str(otid0) == "OpinionTopicID(0)"
    assert otid0 == otid00
    assert otid0 != otid1
    assert otid0 != gid0
    assert otid0 != gabmid0

def test_opinion_topic():
    """
    Test the OpinionTopic class.
    """
    tid = OpinionTopicID(0)
    topic = OpinionTopic(tid, "positive", "A positive opinion.")
    assert topic.id == tid
    assert topic.topic == "positive"
    assert topic.description == "A positive opinion."
    assert "OpinionTopic" in str(topic)
    assert "OpinionTopic" in repr(topic)

def test_opinion_value():
    """
    Test the OpinionValue class.
    """
    tid = OpinionTopicID(0)
    val = OpinionValue(tid, 2, "Strongly positive")
    assert val.opinion_topic_id == tid
    assert val.value == 2
    assert val.description == "Strongly positive"
    assert "OpinionValue" in str(val)
    assert "OpinionValue" in repr(val)

def test_opinion_value_map():
    """
    Test the OpinionValueMap class.
    """
    tid = OpinionTopicID(0)
    val = OpinionValue(tid, 2, "Strongly positive")
    values = OpinionValueMap({tid: val})
    assert values.values[tid] == val
    assert "OpinionValueMap" in str(values)

def test_opinion():
    """
    Test the Opinion class.
    """
    tid = OpinionTopicID(0)
    val = OpinionValue(tid, 2, "Strongly positive")
    values = OpinionValueMap({tid: val})
    opinion = Opinion(tid, values, 2)
    assert opinion.id == tid
    assert opinion.opinion_values == values
    assert opinion.value == 2
    assert "Opinion" in str(opinion)
    assert opinion.get_description() == "Strongly positive"
    opinion2 = Opinion(tid, values, 99) # Value not represented for this opinion topic
    assert opinion2.get_description() is None

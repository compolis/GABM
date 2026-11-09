"""
Tests for election module.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
from datetime import date

# Local imports
from gabm.core.id import GABMID
from gabm.abm.democracy.election import (
    ElectionID,
    Election,
    GeneralElection,
    Referendum,
    VoteID,
    Vote,
)

def test_election_id_and_vote_id_semantics():
    """
    Test the semantics of ElectionID and VoteID classes.
    """
    eid0 = ElectionID(0)
    eid1 = ElectionID(1)
    eid00 = ElectionID(0)
    vid0 = VoteID(0)
    gabmid0 = GABMID(0)

    assert str(eid0) == "ElectionID(0)"
    assert str(vid0) == "VoteID(0)"
    assert eid0 == eid00
    assert eid0 != eid1
    assert eid0 != vid0
    assert eid0 != gabmid0


def test_election_and_subclasses_initialization():
    """
    Test the initialization of Election, GeneralElection, and Referendum objects.
    """
    eid = ElectionID(7)
    d = date(2026, 1, 1)

    election = Election(eid, d, "base election")
    assert election.id == eid
    assert election.date == d
    assert election.description == "base election"

    ge = GeneralElection(ElectionID(8), d, "general election")
    assert ge.id == ElectionID(8)
    assert ge.date == d
    assert ge.description == "general election"

    ref = Referendum(ElectionID(9), d, "referendum", "Question?", ("Yes", "No"))
    assert ref.id == ElectionID(9)
    assert ref.date == d
    assert ref.description == "referendum"
    assert ref.question == "Question?"
    assert ref.choices == ("Yes", "No")


def test_vote_initialization():
    """
    Test the initialization of a Vote object.
    """
    vote = Vote(VoteID(1), ElectionID(2), voter_id="voter-123")

    assert vote.id == VoteID(1)
    assert vote.election_id == ElectionID(2)
    assert vote.voter_id == "voter-123"

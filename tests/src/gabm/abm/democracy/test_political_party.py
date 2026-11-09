"""
Tests for political_party module.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Local imports
from gabm.core.id import GABMID
from gabm.abm.group import OpinionGroup
from gabm.abm.democracy.political_party import PoliticalPartyID, PoliticalParty


def test_political_party_id_semantics():
    """
    Test the semantics of PoliticalPartyID class.
    """
    pid0 = PoliticalPartyID(0)
    pid1 = PoliticalPartyID(1)
    pid00 = PoliticalPartyID(0)
    gabmid0 = GABMID(0)

    assert str(pid0) == "PoliticalPartyID(0)"
    assert str(pid1) == "PoliticalPartyID(1)"
    assert pid0 == pid00
    assert pid0 != pid1
    assert pid0 != gabmid0


def test_political_party_initialization_and_inheritance():
    """
    Test the initialization of a PoliticalParty object and its inheritance from OpinionGroup.
    """
    party = PoliticalParty(PoliticalPartyID(3), "Example Party", "centrist")

    assert isinstance(party, OpinionGroup)
    assert party.id == PoliticalPartyID(3)
    assert party.name == "Example Party"
    assert party.ideology == "centrist"
    assert isinstance(party.opinions, dict)

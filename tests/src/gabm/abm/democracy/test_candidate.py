"""
Tests for candidate module.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
from types import SimpleNamespace

# Local imports
from gabm.abm.environment import Nation
from gabm.abm.democracy.candidate import CandidateID, Candidate

def test_candidate_id():
    """
    Test the CandidateID class.
    """
    c_id = CandidateID(42)
    assert c_id.id == 42

def test_candidate():
    """
    Test the initialization of a Candidate object.
    """
    c_id = CandidateID(42)
    year: int = 2026
    nation = Nation(year=year, name="Test Nation")
    year_of_birth: int = 1975
    candidate = Candidate(c_id, nation, year_of_birth, "candidate description")

    assert candidate.id == c_id
    assert candidate.description == "candidate description"

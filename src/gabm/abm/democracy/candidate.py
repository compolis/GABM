"""
Candidate module for GABM.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import logging
from typing import Dict
# Local imports
from gabm.abm.agent import CitizenID, Citizen
from gabm.abm.environment import Nation

class CandidateID(CitizenID):
    """
    A unique identifier for a Candidate instance.

    Attributes:
        id (int): The unique identifier for the candidate.
    """
    def __init__(self, candidate_id: int):
        super().__init__(candidate_id)

class Candidate(Citizen):
    """
    For representing a candidate.
    
    Attributes:
        candidate_id (CandidateID): Unique identifier for the candidate.
        nation (Nation): The nation the candidate belongs to.
        year_of_birth (int): The year the candidate was born.
        description (str): The description of the candidate.
    """
    def __init__(self, candidate_id: CandidateID, nation: Nation, year_of_birth: int, description: str):
        """
        Initialize a Candidate instance.
        Args:
            candidate_id (CandidateID): The unique identifier for the candidate.
            nation (Nation): The nation the candidate belongs to.
            year_of_birth (int): The year the candidate was born.
            description (str): The description of the candidate.
        """
        super().__init__(candidate_id, nation, year_of_birth)
        self.description = description
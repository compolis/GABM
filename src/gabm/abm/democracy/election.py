"""
Election module for GABM.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import logging
from typing import Dict

class ElectionID(GABMID):
    """
    A unique identifier for an Election instance.
    Attributes:
        election_id (int): The unique identifier for the election.
    """
    def __init__(self, election_id: int):
        super().__init__(election_id)
    
class Election():
    """
    For representing an election.
    Attributes:
        id (ElectionID): Unique identifier for the election.
        year (int): The year of the election.
        description (str): The description of the election.
    """
    def __init__(self, election_id: ElectionID, year: int, description: str):
        """
        Initialize
        Args:
            election_id (ElectionID): The unique identifier for the election.
            year (int): The year of the election.
        """
        self.id = election_id
        self.year = year
        self.description = description


class VoteID(GABMID):
    """
    A unique identifier for a Vote instance.
    Attributes:
        vote_id (int): The unique identifier for the vote.
    """
    def __init__(self, vote_id: int):
        """
        Initialize
        Args:
            vote_id (int): The unique identifier for the vote.
        """
        super().__init__(vote_id)

class Vote():
    """
    For representing a vote.
    Attributes:
        id (VoteID): Unique identifier for the vote.
        description (str): The description of the vote.
    """
    def __init__(self, vote_id: VoteID, description: str):
        """
        Initialize
        Args:
            vote_id (VoteID): The unique identifier for the vote.
            description (str): The description of the vote.
        """
        self.id = vote_id
        self.description = description
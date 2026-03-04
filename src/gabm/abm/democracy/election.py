"""
Election module for GABM.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.2.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import logging
from typing import Dict
from datetime import date
# Local imports
from gabm.core.id import GABMID

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
        date (date): The date of the election.
        description (str): The description of the election.
    """
    def __init__(self, election_id: ElectionID, date: date, description: str):
        """
        Initialize
        Args:
            election_id (ElectionID): The unique identifier for the election.
            date (date): The date of the election.
        """
        self.id = election_id
        self.date = date
        self.description = description

class GeneralElection(Election):
    """
    For representing a general election.
    Attributes:
        id (ElectionID): Unique identifier for the election.
        date (date): The date of the election.
        description (str): The description of the election.
        candidates (Dict[str, str]): A dictionary mapping candidate names to their parties.
    """
    def __init__(self, election_id: ElectionID, date: date, description: str):
        """
        Initialize
        Args:
            election_id (ElectionID): The unique identifier for the election.
            date (date): The date of the election.
            description (str): The description of the election.
        """
        super().__init__(election_id, date, description)

class Referendum(Election):
    """
    For representing a referendum.
    Attributes:
        id (ElectionID): Unique identifier for the referendum.
        date (date): The date of the referendum.
        description (str): The description of the referendum.
        question (str): The question of the referendum.
        choices (tuple[str, ...]): The choices for the referendum.
    """
    def __init__(self, election_id: ElectionID, date: date, description: str, question: str, choices: tuple[str, ...]):
        """
        Initialize
        Args:
            election_id (ElectionID): The unique identifier for the referendum.
            date (date): The date of the referendum.
            description (str): The description of the referendum.
            question (str): The question of the referendum.
            choices (tuple[str, ...]): The choices for the referendum.
        """
        super().__init__(election_id, date, description)
        self.question = question
        self.choices = choices

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
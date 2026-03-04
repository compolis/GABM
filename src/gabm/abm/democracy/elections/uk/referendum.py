"""
UK Referendum module for GABM.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import logging
from typing import Dict
# Local imports
from gabm.core.abm.agent.election import Election, ElectionID, Vote, VoteID

class UKReferendum(Election):
    """
    UK Referendum class, inheriting from the base Election class.
    """
    def __init__(self, election_id: ElectionID, date: str, question: str, choices: tuple[str, ...]):
        """
        Initialize a UK Referendum instance.

        Parameters:
        - election_id: Unique identifier for the referendum.
        - date: Date of the referendum.
        - question: The question being posed in the referendum.
        - choices: The possible choices for the referendum (e.g., "Yes" or "No"). Must be a tuple of strings.
        """
        super().__init__(election_id, date)
        self.question = question
        self.choices = tuple(choices)
        logging.info(f"Initialized UK Referendum with ID {election_id} on {date} with question: {question}")

class UKReferendumVote(Vote):
    """
    UK Referendum Vote class, inheriting from the base Vote class.
    """
    def __init__(self, vote_id: VoteID, election_id: ElectionID, voter_id: str, choice: str):
        """
        Initialize a UK Referendum Vote instance.

        Parameters:
        - vote_id: Unique identifier for the vote.
        - election_id: Identifier for the associated referendum.
        - voter_id: Identifier for the voter.
        - choice: The choice made by the voter (e.g., "Yes" or "No").
        """
        super().__init__(vote_id, election_id, voter_id, choice)
        logging.info(f"Recorded referendum vote {vote_id} for referendum {election_id} by voter {voter_id} with choice {choice}")
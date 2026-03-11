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
from gabm.abm.democracy.election import Election, ElectionID, Vote, VoteID

class UKReferendum(Election):
    """
    UK Referendum class, inheriting from the base Election class.

    A UK Referendum is a specific type of election that takes place in the United Kingdom.
    It is held to allow the electorate to vote on a specific question or issue, rather than
    electing representatives. Referendums can be used to decide on a wide range of issues, 
    such as constitutional changes, membership in international organizations, or specific 
    policy decisions. The outcome of a referendum is typically determined by a simple 
    majority vote, although the specific rules can vary depending on the context and the 
    question being asked.
    """
    def __init__(self, election_id: ElectionID, date: str, question: str, choices: tuple[str, ...]):
        """
        Initialize.

        Args:
            election_id: Unique identifier for the referendum.
            date: Date of the referendum.
            question: The question being posed in the referendum.
            choices: The possible choices for the referendum (e.g., "Yes" or "No"). Must be a tuple of strings.
        """
        super().__init__(election_id, date)
        self.question = question
        self.choices = tuple(choices)
        logging.info(f"Initialized UK Referendum with ID {election_id} on {date} with question: {question}")

class UKReferendumVoteID(VoteID):
    """
    UK Referendum Vote ID class, inheriting from the base VoteID class.
    A UK Referendum Vote ID is a specific type of vote identifier that is used to uniquely identify a vote cast in a UK Referendum.
    Each vote in a UK Referendum is associated with a specific voter and referendum, and the UKReferendumVoteID serves as a unique identifier for that vote.
    """
    def __init__(self, vote_id: int):
        """
        Initialize.

        Args:
            vote_id: Unique identifier for the vote.
        """
        super().__init__(vote_id)
        
class UKReferendumVote(Vote):
    """
    UK Referendum Vote class.

    A UK Referendum Vote is a specific type of vote that takes place during a UK Referendum.
    It is cast by a voter to express their choice on the specific question being posed in the 
    referendum. Each voter typically votes for one of the available choices (e.g., "Yes" or 
    "No"), and the choice with the most votes determines the outcome of the referendum.
    """
    def __init__(self, vote_id: VoteID, election_id: ElectionID, voter_id: str, choice: str):
        """
        Initialize a UK Referendum Vote instance.

        Args:
            vote_id: Unique identifier for the vote.
            election_id: Identifier for the associated referendum.
            voter_id: Identifier for the voter.
            choice: The choice made by the voter (e.g., "Yes" or "No").
        """
        super().__init__(vote_id, election_id, voter_id, choice)
        logging.info(f"Recorded referendum vote {vote_id} for referendum {election_id} by voter {voter_id} with choice {choice}")
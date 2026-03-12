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
from gabm.abm.agent import CitizenID

# Move UKReferendumVoteID above UKReferendum so it is defined before use
class UKReferendumVoteID(VoteID):
    """
    UK Referendum Vote ID
    """
    def __init__(self, vote_id: int):
        """
        Initialize.
        Args:
            vote_id: Unique identifier for the referendum vote.
        """
        super().__init__(vote_id)

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

    .. note::
        Inherits all attributes and methods from :class:`Election`.

    Attributes:
        question (str):
            The question being posed in the referendum.
        choices (tuple[UKReferendumVoteID, ...]):
            The possible choices for the referendum.
    """
    def __init__(self, election_id: ElectionID, date: str, description: str, question: str, choices: tuple[UKReferendumVoteID, ...]):
        """
        Initialize.

        Args:
            election_id: Unique identifier for the referendum.
            date: Date of the referendum.
            description: A brief description of the referendum.
            question: The question being posed in the referendum.
            choices: The possible choices for the referendum.
        """
        super().__init__(election_id, date, description)
        self.question = question
        self.choices = tuple(choices)
        #logging.info(f"Initialized UK Referendum on {date} with ID {election_id}")
        
class UKReferendumVote(Vote):
    """
    UK Referendum Vote class.

    A UK Referendum Vote is a specific type of vote that takes place during a UK Referendum.
    It is cast by a voter to express their choice on the specific question being posed in the 
    referendum. Each voter typically votes for one of the available choices (e.g., "Yes" or 
    "No"), and the choice with the most votes determines the outcome of the referendum.

    .. note::
        Inherits all attributes and methods from :class:`Vote`.
    """
    def __init__(self, vote_id: UKReferendumVoteID, election_id: ElectionID, voter_id: CitizenID = None):
        """
        Initialize a UK Referendum Vote instance.

        Args:
            vote_id:
                Unique identifier for the vote.
            election_id:
                Identifier for the associated referendum.
            voter_id:
                Identifier for the voter.
        """
        super().__init__(vote_id, election_id, voter_id)
        #logging.info(f"Recorded referendum vote {vote_id} for referendum {election_id} by voter {voter_id}")
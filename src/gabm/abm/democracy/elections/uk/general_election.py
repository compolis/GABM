"""
UK General Election module for GABM.
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

class UKGE(Election):
    """
    UK General Election (UKGE) class, inheriting from the base Election class.
    """
    def __init__(self, election_id: ElectionID, date: date):
        """
        Initialize a UK General Election instance.

        Parameters:
        - election_id: Unique identifier for the election.
        - date: Date of the election.
        """
        super().__init__(election_id, date.year)
        logging.info(f"Initialized UKGE with ID {election_id} on {date} with candidates: {candidates}") 
    
class UKGEVote(Vote):
    """
    UK General Election Vote class, inheriting from the base Vote class.
    """
    def __init__(self, vote_id: VoteID, election_id: ElectionID, voter_id: str, candidate_id: str):
        """
        Initialize a UK General Election Vote instance.

        Parameters:
        - vote_id: Unique identifier for the vote.
        - election_id: Identifier for the associated election.
        - voter_id: Identifier for the voter.
        - candidate_id: Identifier for the candidate being voted for.
        """
        super().__init__(vote_id, election_id, voter_id, candidate_id)
        logging.info(f"Recorded vote {vote_id} for election {election_id} by voter {voter_id} for candidate {candidate_id}")

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
from datetime import date
# Local imports
from gabm.abm.democracy.election import Election, ElectionID, Vote, VoteID

class UKGE(Election):
    """
    UK General Election (UKGE) class, inheriting from the base Election class.

    A UK General Election is a specific type of election that takes place in the United Kingdom.
    It is held to elect Members of Parliament (MPs) to the House of Commons, which is the lower house of the UK Parliament.
    The election typically occurs every five years, although it can be called earlier under certain circumstances.
    """
    def __init__(self, election_id: ElectionID, date: date):
        """
        Initialize.

        Args:
            election_id: Unique identifier for the election.
            date: Date of the election.
        """
        super().__init__(election_id, date.year)
        logging.info(f"Initialized UKGE with ID {election_id} on {date} with candidates: {candidates}") 

class UKGEVoteID(VoteID):
    """
    UK General Election Vote ID class, inheriting from the base VoteID class.
    A UK General Election Vote ID is a specific type of vote identifier that is used to uniquely identify a vote cast in a UK General Election.
    Each vote in a UK General Election is associated with a specific voter, candidate, and election, and the UKGEVoteID serves as a unique identifier for that vote.
    """
    def __init__(self, vote_id: int):
        """
        Initialize.

        Args:
            vote_id: Unique identifier for the vote.
        """
        super().__init__(vote_id)
        
class UKGEVote(Vote):
    """
    UK General Election Vote.
    
    A UK General Election Vote is a specific type of vote that takes place during a UK General Election.
    It is cast by a voter to elect a candidate to represent their constituency in the House of Commons.
    Each voter typically votes for one candidate in their constituency, and the candidate with the most
    votes in each constituency wins a seat in the House of Commons.
    """
    def __init__(self, vote_id: VoteID, election_id: ElectionID, voter_id: str, candidate_id: str):
        """
        Initialize a UK General Election Vote instance.

        Args:
            vote_id: Unique identifier for the vote.
            election_id: Identifier for the associated election.
            voter_id: Identifier for the voter.
            candidate_id: Identifier for the candidate being voted for.
        """
        super().__init__(vote_id, election_id, voter_id, candidate_id)
        logging.info(f"Recorded vote {vote_id} for election {election_id} by voter {voter_id} for candidate {candidate_id}")

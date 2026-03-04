"""
Political Party module for GABM.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import logging
# Local imports
from gabm.core.id import GABMID

class PoliticalPartyID(GABMID):
    """
    A unique identifier for a PoliticalParty instance.
    Attributes:
        party_id (int): The unique identifier for the political party.
    """
    def __init__(self, party_id: int):
        super().__init__(party_id)


class PoliticalParty(OpinionatedGroup):
    """
    For representing a political party.
    Attributes:
        id (PoliticalPartyID): Unique identifier for the political party.
        name (str): The name of the political party.
        ideology (str): The ideology of the political party.
    """
    def __init__(self, party_id: PoliticalPartyID, name: str, ideology: str):
        """
        Initialize a PoliticalParty instance.
        Args:
            party_id (PoliticalPartyID): The unique identifier for the political party.
            name (str): The name of the political party.
            ideology (str): The ideology of the political party.
        """
        super().__init__(party_id, name)
        self.ideology = ideology
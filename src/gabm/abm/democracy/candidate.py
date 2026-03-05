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
from gabm.abm.agent import AgentID, Citizen

class Candidate(Citizen):
    """
    For representing a candidate.
    Attributes:
        id (AgentID): Unique identifier for the candidate.
        description (str): The description of the candidate.
    """
    def __init__(self, agent_id: AgentID, description: str):
        """
        Initialize a Candidate instance.
        Args:
            agent_id (AgentID): The unique identifier for the candidate.
            description (str): The description of the candidate.
        """
        self.id = agent_id
        self.description = description
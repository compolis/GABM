"""
Defines the generic Environment class.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Standard library imports
from typing import Dict
# Local imports
from gabm.abm.agents.agent import Agent
from gabm.abm.agents.group import Group

class Environment:

    def __init__(self):
        """
        Initialize the environment.
        """
        self.agents_active: Dict[int, Agent] = {}
        self.agents_inactive: Dict[int, Agent] = {}
        self.groups_active: Dict[int, Group] = {}
        self.groups_inactive: Dict[int, Group] = {}
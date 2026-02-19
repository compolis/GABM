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
    """
    The Environment class represents the shared context in which agents and groups interact.
    It can be extended to represent specific types of environments (e.g., a Nation).
    Attributes:
        year (int): The current year in the simulation.
        place (str): The name of the place or environment.
        agents_active (Dict[int, Agent]): A dictionary of active agents, keyed by their unique id.
        agents_inactive (Dict[int, Agent]): A dictionary of inactive agents, keyed by their unique id.
        groups_active (Dict[int, Group]): A dictionary of active groups, keyed by their unique id.
        groups_inactive (Dict[int, Group]): A dictionary of inactive groups, keyed by their unique id.
    """

    def __init__(self, year: int = 2026, place: str = "Earth"):
        """
        Initialize the environment.
        Args:
            year: The current year in the simulation.
            place: The name of the place or environment.
        """
        self.year = year
        self.place = place
        self.agents_active: Dict[int, Agent] = {}
        self.agents_inactive: Dict[int, Agent] = {}
        self.groups_active: Dict[int, Group] = {}
        self.groups_inactive: Dict[int, Group] = {}

class Opinionated_Environment(Environment):
    """
    An extension of the Environment class that includes opinions.
    Attributes:
        opinions (Dict[str, str]): A dictionary to hold opinions.
        The key is a short name, the value is a description.
    """
    def __init__(self, year: int = 2026, place: str = "Earth"):
        super().__init__(year=year, place=place)
        self.opinions = {}

class Nation(Opinionated_Environment):
    """
    A specific type of Opinionated_Environment representing a nation.
    Can be extended with nation-specific attributes and methods.
    Attributes:
        opinions (Dict[str, str]): A dictionary to hold opinions.
        The key is a short name, the value is a description.
        nation (str): The name of the nation (e.g., "United Kingdom").
    """
    def __init__(self, name: str, year: int = 2026, nation: str = "United Kingdom"):
        """
        Initialize a Nation environment.
        Args:
            name: The name of the nation.
            year: The current year in the simulation.
            nation: The name of the nation (e.g., "United Kingdom").
        """
        super().__init__(year=year, place=name)
        self.nation = nation
        self.opinions = {}
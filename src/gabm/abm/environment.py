"""
Environment module for GABM.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.2.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Standard library imports
from typing import Dict
# Local imports
from gabm.abm.agent import Agent
from gabm.abm.group import Group
from gabm.abm.opinion import OpinionID, OpinionValue, OpinionValues, Opinion

class Environment:
    """
    Represents the shared context in which Agent instances interact.
    It can be extended to represent specific types of environment.
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

class OpinionatedEnvironment(Environment):
    """
    An Environment with opinions.
    Attributes:
        opinions (Dict[OpinionID, Opinion]): A dictionary of opinions.
        The key is an OpinionID, the value is an Opinion object.
    """

    def __init__(self, year: int = 2026, place: str = "Earth",
        opinions: Dict[OpinionID, Opinion] = None):
        """
        Initialize an OpinionatedEnvironment.
        Args:
            year: The current year in the simulation.
            place: The name of the place or environment.
            opinions: A dictionary of opinions, where the key is an OpinionID and the value is an Opinion object.
             This allows the environment to have an overview of opinions of Persons and OpinionatedGroups.
        """
        super().__init__(year=year, place=place)
        self.opinions = opinions if opinions is not None else {}

    def get_AverageOpinion(self, opinion_topic_id: OpinionTopicID) -> float:
        """
        Get the average opinion value of the group members on a specific topic.
        Args:
            opinion_topic_id: The opinion topic ID to get the average opinion on.
        Return:
            The average opinion value for the topic, or None if no members have an opinion on it.
        """

class Nation(OpinionatedEnvironment):
    """
    An OpinionatedEnvironment representing a nation.
    Can be extended with nation-specific attributes and methods.
    Attributes:
        nation (str): The name of the nation (e.g., "United Kingdom").
    """
    
    def __init__(self, year: int = 2026, place: str = "Earth", 
        opinions: Dict[OpinionID, Opinion] = None, nation: str = "United Kingdom"):
        """
        Initialize a Nation environment.
        Args:
            year: The current year in the simulation.
            place: The name of the place or environment.
            opinions: A dictionary of opinions, where the key is an OpinionID and the value is an Opinion object.
             This allows the nation to have an overview of opinions of Persons and OpinionatedGroups.
            nation: The name of the nation (e.g., "United Kingdom").
        """
        super().__init__(year=year, place=place, opinions=opinions)
        self.nation = nation
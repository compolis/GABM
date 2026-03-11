"""
Environment module for GABM.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.3.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
from typing import Dict
# Local imports
from gabm.abm.agent import Agent
from gabm.abm.attributes.opinion import OpinionTopicID, OpinionValue, OpinionValueMap, Opinion
from gabm.abm.group import Group
from gabm.abm.attributes.gender import GenderMap

class Environment():
    """
    An Environment with opinions.

    Attributes:
        year (int):
            The current year in the simulation.
        place (str):
            The name of the place or environment.
        agents_active (Dict[AgentID, Agent]):
            A dictionary of active agents in the environment.
        agents_inactive (Dict[AgentID, Agent]):
            A dictionary of inactive agents in the environment.
        groups_active (Dict[GroupID, Group]):
            A dictionary of active groups in the environment.
        groups_inactive (Dict[GroupID, Group]):
            A dictionary of inactive groups in the environment.
        gender_map (GenderMap):
            A map for gender attribute lookups.
        opinions (Dict[OpinionTopicID, Opinion]):
            A dictionary of opinions.
            The key is an OpinionTopicID, the value is an Opinion object.
    """

    def __init__(self, year: int = 2026, place: str = "Earth",
        gender_map: GenderMap = None,
        opinions: Dict[OpinionTopicID, Opinion] = None):
        """
        Initialize.

        Args:
            year (int):
                The current year in the simulation.
            place (str):
                The name of the place or environment.
            gender_map (GenderMap):
                A GenderMap instance for gender attribute lookups.
            opinions (Dict[OpinionTopicID, Opinion]):
                A dictionary of opinions, where the key is an OpinionTopicID and the value is an Opinion object.
                This allows the environment to have an overview of opinions of Persons and OpinionatedGroups.
            
        """
        self.year = year
        self.place = place
        self.agents_active: Dict = {}
        self.agents_inactive: Dict = {}
        self.groups_active: Dict = {}
        self.groups_inactive: Dict = {}
        self.opinions = opinions if opinions is not None else {}
        self.gender_map = gender_map if gender_map is not None else GenderMap()

    def __str__(self):
        """
        Return:
            A string representation.
        """
        class_name = self.__class__.__name__
        return f"{class_name}: year={self.year}, place='{self.place}', " \
               f"agents_active={len(self.agents_active)}, agents_inactive={len(self.agents_inactive)}, " \
               f"groups_active={len(self.groups_active)}, groups_inactive={len(self.groups_inactive)}, " \
               f"opinions={len(self.opinions)}, gender_map={self.gender_map}"

    def __repr__(self):
        """
        Return:
            An official string representation.
        """
        return self.__str__()

class Nation(Environment):
    """
    An Environment representing a nation.
    Can be extended with nation-specific attributes and methods.
    
    .. note::
            Inherits all attributes from :class:`Environment`.

    Attributes:
        citizens (Group):
            A group of Person agents representing the citizens of the nation.
        aliens (Group):
            A group of Person agents representing the aliens in the nation.
    """
    
    def __init__(self, year: int = 2026, place: str = "Earth", 
        gender_map: GenderMap = None, opinions: Dict[OpinionTopicID, Opinion] = None, nation: str = "United Kingdom"):
        """
        Initialize.
        Args:
            year (int):
                The current year in the simulation.
            place (str):
                The name of the nation.
            gender_map (GenderMap):
                A GenderMap instance for gender attribute lookups.
            opinions (Dict[OpinionTopicID, Opinion]):
                A dictionary of opinions, where the key is an OpinionTopicID and the value is an Opinion object.
                This allows the environment to have an overview of opinions of Persons and OpinionatedGroups.
        
        """
        super().__init__(year=year, place=place, gender_map=gender_map, opinions=opinions)
        from gabm.abm.group import Group, GroupID
        self.citizens = Group(GroupID(1), name="Citizens")
        self.groups_active[self.citizens.id] = self.citizens
        self.aliens = Group(GroupID(2), name="Aliens")
        self.groups_active[self.aliens.id] = self.aliens
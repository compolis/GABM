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
        opinions (Dict[OpinionTopicID, Opinion]): A dictionary of opinions.
        The key is an OpinionTopicID, the value is an Opinion object.
    """

    def __init__(self, year: int = 2026, place: str = "Earth",
        opinions: Dict[OpinionTopicID, Opinion] = None,
        gender_map: GenderMap = None):
        """
        Initialize an OpinionatedEnvironment.

        Args:
            year (int):
                The current year in the simulation.
            place (str):
                The name of the place or environment.
            opinions (Dict[OpinionTopicID, Opinion]):
                A dictionary of opinions, where the key is an OpinionTopicID and the value is an Opinion object.
                This allows the environment to have an overview of opinions of Persons and OpinionatedGroups.
            gender_map (GenderMap):
                A GenderMap instance for gender attribute lookups.
        """
        super().__init__(year=year, place=place)
        self.opinions = opinions if opinions is not None else {}
        self.gender_map = gender_map if gender_map is not None else GenderMap()

    def __str__(self):
        """
        Return:
            A string representation.
        """
        return f"Environment(year={self.year}, place='{self.place}', " \
               f"agents_active={len(self.agents_active)}, agents_inactive={len(self.agents_inactive)}, " \
               f"groups_active={len(self.groups_active)}, groups_inactive={len(self.groups_inactive)}, " \
               f"opinions={len(self.opinions)})"

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
    
    Attributes:
        nation (str): The name of the nation (e.g., "United Kingdom").
        citizens (Group): A group of Person agents representing the citizens of the nation.
        aliens (Group): A group of Person agents representing the aliens in the nation.
    """
    
    def __init__(self, year: int = 2026, place: str = "Earth", 
        opinions: Dict[OpinionTopicID, Opinion] = None, nation: str = "United Kingdom"):
        """
        Initialize a Nation environment.
        Args:
            year (int):
                The current year in the simulation.
            place (str):
                The name of the place or environment.
            opinions (Dict[OpinionTopicID, Opinion]):
                A dictionary of opinions, where the key is an OpinionTopicID and the value is an Opinion object.
                This allows the environment to have an overview of opinions of Persons and OpinionatedGroups.
            gender_map (GenderMap):
                A GenderMap instance for gender attribute lookups.

        """
        super().__init__(year=year, place=place, opinions=opinions)
        self.nation = nation
        self.citizens = Group()  # type: Group
        self.groups_active.append(self.citizens)  # type: ignore
        self.aliens = Group()  # type: Group
        self.groups_active.append(self.aliens)  # type: ignore

    def __str__(self):
        """
        Return:
            A string representation.
        """
        return f"Nation(nation='{self.nation}', year={self.year}, place='{self.place}', " \
               f"agents_active={len(self.agents_active)}, agents_inactive={len(self.agents_inactive)}, " \
               f"groups_active={len(self.groups_active)}, groups_inactive={len(self.groups_inactive)}, opinions={len(self.opinions)})"

    def __repr__(self):
        """
        Return:
            An official string representation.
        """
        return self.__str__()
# NOTE: This import must be the very first non-empty line in the file (even before docstrings)
# due to Python syntax rules for __future__ imports.
from __future__ import annotations
"""
Agent module for GABM.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.2.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Standard library imports
from typing import TYPE_CHECKING, Set
from gabm.abm.opinion import Opinion, OpinionTopicID, OpinionValue, OpinionValues
import copy
import logging
# TYPE_CHECKING is used to avoid circular imports.
if TYPE_CHECKING:
    from gabm.abm.attributes.ethnicity import EthnicityID, 
    from gabm.abm.attributes.gender import GenderID, Gender, GenderMap
    from gabm.abm.attributes.opinion import OpinionTopicID, OpinionValue, OpinionValues, Opinion
    from gabm.abm.environment import Environment, OpinionatedEnvironment
    from gabm.abm.group import Group, OpinionatedGroup


class AgentID():
    """
    A unique identifier for an Agent instance.
    Attributes:
        agent_id (int): The unique identifier for the agent.
    """
    def __init__(self, agent_id: int):
        self.id = agent_id

    def __str__(self):
        """
        Return:
            A string representation.
        """
        return f"AgentID({self.id})"

    def __repr__(self):
        """
        Return:
            A string representation.
        """
        return self.__str__()

class Agent():
    """
    For representing an entity within an Environment. 
    The type annotation for environment is quoted as it is imported 
    under TYPE_CHECKING to avoid circular imports.
    Attributes:
        agent_id (AgentID): Unique identifier for the Agent instance.
        environment (Environment): The Environment the Agent instance belongs to.
        groups (Set[Group]): A Set of Groups that the Agent instance belongs to.
    """
    def __init__(self, agent_id: AgentID, environment: "Environment"):
        """
        Initialize.
        Args:
            agent_id: Unique identifier for the Agent instance.
            environment: The shared environment the Agent instance belongs to.
        """
        self.id = agent_id
        self.environment = environment
        self.groups: Set['Group'] = set()

    def __str__(self):
        """
        Return:
            String representation.
        """
        return f"Agent (id={self.id}, groups={len(self.groups)})" 
    
    def __repr__(self):
        """
        Return:
            Official String representation.
        """
        return self.__str__()

    def join_group(self, group: 'Group'):
        """
        Join group. (This updates group membership.)
        Args:
            group: The Group instance to join.
        """
        group.add_member(self)

    def leave_group(self, group: 'Group'):
        """
        Leave group. (This updates group membership.)
        Args:
            group: The Group instance to leave.
        """
        group.remove_member(self)

class Animal(Agent):
    """
    An Agent with a year of birth and Gender.
    The type annotation for environment is quoted as it is imported 
    under TYPE_CHECKING to avoid circular imports.
    Attributes:
        year_of_birth (int): The year of birth attributed.
        gender_map (Dict[GenderID, Gender]): A mapping of GenderIDs to Genders, used to interpret the gender value.
         This allows the gender to be represented as an integer internally, but interpreted as a string when needed.
         The default mapping includes:
            0: "female",
            1: "male",
            2: "non-binary",
            None: "none".
         This mapping can be extended to include more genders as needed.
         The gender value is stored as an integer (e.g., 0, 1, 2) for efficiency, but the gender_map allows for 
         interpretation of the gender as a string (e.g., "female", "male", "non-binary").
        gender (Gender): The gender attributed.
    """
    def __init__(self, agent_id: AgentID, environment: "Environment",
        year_of_birth: int = None, gender_map: Dict[GenderID, Gender] = None,
        gender: Gender = None):
        """
        Initialize. If year of birth is none, then the instance is 
        initialised with a year of birth that would make them 18 years 
        old in the current year of the environment. If year_of_birth 
        is a value greater than environment.year, then self.year_of_birth
        is set to the current year in the environment with a warning. 
        This avoids having agents with negative ages when initialised.
        Args:
            agent_id: Unique identifier for the Agent instance.
            environment: The shared environment the Agent instance belongs to.   
            year_of_birth: The year the animal was born.
            gender_map: A mapping of GenderIDs to Genders, used to interpret the gender.
            gender: The Gender of the animal.
        """
        super().__init__(agent_id, environment)
        self.gender = gender
        self.gender_map = gender_map
        # Raise a warning if gender is not in the gender map
        if self.gender is not None and self.gender_map is None:
            message = f"Gender value {self.gender} is provided but no gender map is provided. Cannot interpret gender value."
            logging.warning(message)
            raise ValueError(message)
        # Raise a warning if gender is not in the gender map (if gender map is provided).
        if self.gender is not None and self.gender_map is not None and self.gender not in self.gender_map:
            message = f"Gender value {self.gender} is not in the gender map. Valid gender values are: {list(self.gender_map.keys())}. Setting gender to None."
            logging.warning(message)
            raise ValueError(message)
        if year_of_birth is None:
            self.year_of_birth = self.environment.year - 18
        else:
            self.year_of_birth = year_of_birth
            """
            If year_of_birth is greater than the current year set year 
            of birth to be the current year from the environment.
            """
            if self.year_of_birth > self.environment.year:
                logging.warning(f"year_of_birth ({self.year_of_birth}) cannot be greater than the current year ({self.environment.year}). Setting year_of_birth to {self.environment.year}.")
                self.year_of_birth = self.environment.year

    def __str__(self):
        """
        Return:
            String representation.
        """
        super_str = super().__str__()
        return f"{super_str}, year_of_birth={self.year_of_birth}, gender={self.get_gender()}"

    def __repr__(self):
        """
        Return: 
            Official string representation.
        """
        return self.__str__()

    def get_age(self) -> int:
        """
        Get the age in years based on the current year in the environment.
        Return:
            Age in years, or None if year_of_birth is not set.
        """
        if self.year_of_birth is None:
            return None
        return self.environment.year - self.year_of_birth

    def get_gender(self) -> str:
        """
        Get the gender as a string.
        Return:
            Gender as a string.
        """
        if self.gender is None:
            return "none"
        return self.gender_map.get(self.gender)

class Person(Animal):
    """
    An Animal with opinions that is part of an OpinionatedEnvironment.
    Attributes:
        opinions: A dictionary of Opinions.
         The keys are OpinionTopicIDs, and the values are Opinion objects.
         These are deep copied when the Person is initialised, so that the Person has their own opinions.
    """
    def __init__(self, agent_id: AgentID, environment: "OpinionatedEnvironment",
        year_of_birth: int = None, gender_map: Dict[GenderID, Gender] = None,
        gender: Gender = None,  opinions: dict[OpinionTopicID, 'Opinion'] = None):
        """
        Initialize
        Args:
            agent_id: Unique identifier for the Agent instance.
            environment: The Environment the Agent instance belongs to.
            year_of_birth: The year the animal was born.
            gender_map: The map of gender IDs to Gender objects.
            gender: The gender attributed.
            opinions: A dictionary of opinions, where keys are OpinionTopicIDs and values are Opinion objects.
        """
        super().__init__(agent_id, environment, year_of_birth=year_of_birth, gender_map=gender_map,  gender=gender)
        if self.get_age() > 200:
            logging.warning(f"Age ({self.get_age()}) is unusually high.")
        self.opinions = {}
        # If opinions are provided, deep copy them to the person so that they have their own opinions.
        if opinions is not None:
            for opinion_topic_id, opinion in opinions.items():
                self.opinions[opinion_topic_id] = copy.deepcopy(opinion)
        
    def __str__(self):
        """
        Return:
            String representation.
        """
        super_str = super().__str__()
        return f"{super_str}, opinions={self.opinions}"

    def __repr__(self):
        """
        Return: 
            Official string representation.
        """
        return self.__str__()
        
    def get_opinion(self, opinion_id: OpinionTopicID) -> 'Opinion':
        """
        Args:
            opinion_id: The ID of the opinion to get.
        Return:
            The Opinion object for the opinion_id, or None if not found.
        """
        return self.opinions.get(opinion_id)

    def add_opinion(self, opinion: 'Opinion', value: OpinionValue):
        """
        Add opinion to opinions.
        Args:
            opinion: The Opinion to add.
            value: The OpinionValue to add for the opinion.
        """
        self.opinions[opinion.opinion_id] = opinion
        self.opinions[opinion.opinion_id].value = value

    def set_opinion(self, opinion_id: OpinionTopicID, value: OpinionValue):
        """
        Set an opinion value.
        Args:
            opinion_id: The ID of the opinion to set.
            value: The value to set the opinion to.
        """
        if opinion_id not in self.opinions:
            message = (f"Attempting to set opinion value for non-existent opinion ID {opinion_id}. "
                       f"Valid opinion IDs are: {list(self.opinions.keys())}. "
                       f"Adding new opinion with value {value}.")
            logging.warning(message)
            raise ValueError(message)
        else:
            self.opinions[opinion_id].value = value

    def get_opinion_profile(self) -> str:
        """
        An opinion profile is a summary of opinions reflecting the similarity and difference 
        in opinions of the individual relative to their groups and others in the enviornment.
        Return:
            A string summarizing the opinion profile.
        """
        if len(self.opinions) == 0:
            return "I have no opinions."
        # Return a simple summary what the opinions are.
        summary = "I have opinions about the following topics:\n"
        for topic, value in self.opinions.items():
            summary += f"  {topic}\n"
        return summary

    def get_self_description(self) -> str:
        """
        Get a self-description of the person.
        Return:
            A string describing the person.
        """
        age = self.get_age()
        desc = f"I am {age} years old. "
        if self.gender is not None:
            desc += f"I am {self.get_gender()}. "
        return desc

    def communicate(self, i: int):
        """
        Communicate with another agent.
        Args:
            i: The index of the agent to communicate with.
        Note:
            This method should only be used when both self and the other agent are instances of Person
            (i.e., have an 'opinions' attribute). If not, the method will log a warning and do nothing.
        """
        other_agent = self.environment.agents_active[i]
        if not (hasattr(self, 'opinions') and hasattr(other_agent, 'opinions')):
            logging.warning(f"communicate called with non-Person agent(s): self={type(self)}, other_agent={type(other_agent)}. Skipping communication.")
            return
        logging.info(f"{self} is communicating with {other_agent}")
        # If either agent is in the Neutral group, update the neutral agents opinions to the average
        neutral_groups = [group for group in self.environment.groups_active.values() if group.name == "Neutral"]
        self_in_neutral = any(self in group.members for group in neutral_groups)
        other_in_neutral = any(other_agent in group.members for group in neutral_groups)
        if self_in_neutral or other_in_neutral:
            # Build averaged opinions for all topics
            avg_opinions = {}
            for topic in set(self.opinions.keys()).union(other_agent.opinions.keys()):
                self_opinion = self.opinions.get(topic, None)
                other_opinion = other_agent.opinions.get(topic, None)
                self_val = self_opinion.value if self_opinion is not None else 0
                other_val = other_opinion.value if other_opinion is not None else 0
                avg_value = int(round((self_val + other_val) / 2))
                # Use self's opinion_values if available, else other's, else None
                opinion_values = None
                if self_opinion is not None:
                    opinion_values = self_opinion.opinion_values
                elif other_opinion is not None:
                    opinion_values = other_opinion.opinion_values
                else:
                    opinion_values = None
                avg_opinions[topic] = Opinion(topic, opinion_values, avg_value)
            if self_in_neutral:
                self.opinions = {topic: opinion for topic, opinion in avg_opinions.items()}
                logging.info(f"{self} is in the Neutral group, so opinion is updated to the average of { {k: v.value for k, v in avg_opinions.items()} }")
            if other_in_neutral:
                other_agent.opinions = {topic: opinion for topic, opinion in avg_opinions.items()}
                logging.info(f"{other_agent} is in the Neutral group, so opinion is updated to the average of { {k: v.value for k, v in avg_opinions.items()} }")
    
    def communicate_with_llm(self, message: str, model: str = None) -> dict:
        """
        Communicate with an LLM to get a response based on the input message and model.
        Args:
            message: The prompt to send to the LLM.
            model: The name of the LLM model to use (optional).
        Return:
            The response from the LLM as a dictionary, or None if an error occurs
        """
        # For now, we will just return a dummy response.
        # In the future, this method can be implemented to call an actual LLM API.
        return {"response": f"Echo: {message}", "model": model}

class Citizen(Person):
    """
    A Person who belongs to a Nation.
    """
    def __init__(self, agent_id: int, environment: "Nation",
        year_of_birth: int = None, gender_map: Dict[GenderID, Gender] = None,
        gender: Gender = None, opinions: dict = None):
        """
        Args:
            agent_id: Unique identifier for the agent.
            environment: The Nation the agent belongs to.
            year_of_birth: Year of birth (int).
            gender_map: The map of gender IDs to Gender objects.
            gender: The gender attributed.
            opinions: A dictionary of opinions, where keys are OpinionTopicIDs and values are Opinion objects.
        """
        super().__init__(agent_id, environment, year_of_birth=year_of_birth,
            gender_map=gender_map, gender=gender, opinions=opinions)

class Alien(Person):
    """
    A Person who does not belong to a Nation.
    """
    def __init__(self, agent_id: int, environment: "Nation",
        year_of_birth: int = None, gender_map: Dict[GenderID, Gender] = None,
        gender: Gender = None, opinions: dict = None):
        """
        Args:
            agent_id: Unique identifier for the agent.
            environment: The Nation the agent belongs to.
            year_of_birth: Year of birth (int).
            gender_map: The map of gender IDs to Gender objects.
            gender: The gender attributed.
            opinions: A dictionary of opinions, where keys are OpinionTopicIDs and values are Opinion objects.
        """
        super().__init__(agent_id, environment, year_of_birth=year_of_birth,
            gender_map=gender_map, gender=gender, opinions=opinions)
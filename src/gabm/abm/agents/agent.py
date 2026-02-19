# NOTE: This import must be the very first non-empty line in the file (even before docstrings)
# due to Python syntax rules for __future__ imports.
from __future__ import annotations
"""
Defines the generic Agent class.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Standard library imports
from typing import TYPE_CHECKING, Set
import logging
# TYPE_CHECKING is used to avoid circular imports.
if TYPE_CHECKING:
    from gabm.abm.environment import Environment, Opinionated_Environment
    from gabm.abm.agents.group import Group, Opinionated_Group

class Agent:
    """
    An Agent is an entity within an Enviornment.
    Attributes:
        id (int): Unique identifier for the agent.
        environment (Environment): The shared environment the agent belongs to.
        groups (Set[Group]): A set of groups that the agent belongs to.
    """
    def __init__(self, agent_id: int, environment: Environment, opinion: float = 0.0):
        """
        Initialize.
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
        Join a group and update the group's membership.
        Args:
            group: The Group instance to join.
        """
        group.add_member(self)

    def leave_group(self, group: 'Group'):
        """
        Leave a group and update the group's membership.
        Args:
            group: The Group instance to leave.
        """
        group.remove_member(self)

class Animal(Agent):
    """
    Animal is an Agent with a year of birth and gender.
    Attributes:
        year_of_birth (int): The year the animal was born.
        gender (int): The gender of the animal (0 is female, 1 is male, 2 is non-binary, None is not set).  
    """
    def __init__(self, agent_id: int, environment: Environment,
        year_of_birth: int = None, gender: int = None):
        """
        Initialize
        If year of birth is none, then the person is initialised with a 
        year of birth that would make them 18 years old in the current 
        year of the environment. This is just a default assumption to 
        give them an age, but it can be overridden by providing a 
        specific year_of_birth.
        """
        super().__init__(agent_id, environment)
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
        self.gender = gender

    def __str__(self):
        """
        Return:
            String representation of the Person.
        """
        super_str = super().__str__()
        return f"{super_str}, year_of_birth={self.year_of_birth}, gender={self.get_Gender()}"

    def __repr__(self):
        """
        Return: 
            Official string representation of the Person.
        """
        return self.__str__()

    def get_Age(self) -> int:
        """
        Get the age in years based on the current year in the environment.
        Return:
            Age in years, or None if year_of_birth is not set.
        """
        if self.year_of_birth is None:
            return None
        return self.environment.year - self.year_of_birth

    def get_Gender(self) -> str:
        """
        Get the gender as a string.
        Return:
            Gender as a string.
        """
        if self.gender is None:
            return "not set"
        gender_map = {0: "female", 1: "male", 2: "non-binary"}
        return gender_map[self.gender]

class Person(Animal):    
    """
    A Person is an Animal with opinions that is part of an Opinionated_Environment.
    Attributes:
        opinions: A dictionary of opinions on various topics.
        The key is a short name for the topic, and the value is an int opinion value.
        (e.g., {"positive": 5}, {"neutral": 0}, {"negative": -3}).
    """
    def __init__(self, agent_id: int, environment: "Opinionated_Environment",
        year_of_birth: int = None, gender: int = None,
        opinions: dict = None):
        """
        Initialize
        """
        super().__init__(agent_id, environment, year_of_birth=year_of_birth)
        if self.get_Age() > 200:
            logging.warning(f"Age ({self.get_Age()}) is unusually high. Setting year_of_birth to be 200 years ago.")
            self.year_of_birth = self.environment.year - 200
        self.opinions = opinions

    def __str__(self):
        """
        Return:
            String representation of the Person.
        """
        super_str = super().__str__()
        return f"{super_str}, opinions={self.opinions}"

    def __repr__(self):
        """
        Return: 
            Official string representation of the Person.
        """
        return self.__str__()
        
    def get_Opinion(self, topic: str) -> int:
        """
        Get the opinion value on a specific topic.
        Args:
            topic: The topic to get the opinion on.
        Return:
            The opinion value for the topic, or None if not set.
        """
        if self.opinions is None:
            return None
        return self.opinions.get(topic)

    def set_Opinion(self, topic: str, value: int):
        """
        Set the opinion on a specific topic.
        Args:
            topic: The topic to set the opinion on. This should have a record in env. 
            value: The opinion value to set for the topic.
        """
        if self.opinions is None:
            self.opinions = {}
        self.opinion[topic] = value

    def update_Opinion(self, topic: str, delta: int):
        """
        Update the opinion of the person on a specific topic by adding a delta value.
        Args:
            topic: The topic to update the opinion on.
            delta: The value to add to the existing opinion for the topic.
        """
        if self.opinions is None:
            self.opinions = {}
        current_value = self.opinions.get(topic, 0)
        self.opinion[topic] = current_value + delta

    def get_opinion_profile(self) -> str:
        """
        Return:
            A string summarizing the opinion_profile.
        """
        if self.opinions is None:
            return "I have no opinions."
        """
        An opinion profile is a summary of opinions focussing on what is more unusual.
        What is unusual can be defined as opinions that are more extreme in value 
        compared to those of a group. The number of opinions may be a factor in the profile.
        The proportion of more extreme opinions can also be important for the profile.
        """
        # For the time being, return a simple summary what the opinions are.
        summary = "I have opinions about the following topics:\n"
        for topic, value in self.opinion.items():
            summary += f"  {topic}\n"
        return summary

    def get_self_description(self) -> str:
        """
        Get a self-description of the person.
        Return:
            A string describing the person.
        """
        age = self.get_Age()
        desc = f"I am {age} years old. "
        if self.gender is not None:
            desc += f"I am {self.get_Gender()}. "
        return desc

    def communicate(self, i: int):
        """
        Communicate with another agent.
        Args:
            i: The index of the agent to communicate with.
        """
        other_agent = self.environment.agents_active[i]
        logging.info(f"{self} is communicating with {other_agent}")
        # If either agent is in the Neutral group, update the neutral agents opinions to the average
        neutral_groups = [group for group in self.environment.groups_active.values() if group.name == "Neutral"]
        self_in_neutral = any(self in group.members for group in neutral_groups)
        other_in_neutral = any(other_agent in group.members for group in neutral_groups)
        if self_in_neutral or other_in_neutral:
            # Build averaged opinions for all topics
            avg_opinions = {}
            for topic in set(self.opinions.keys()).union(other_agent.opinions.keys()):
                self_val = self.opinions.get(topic, 0)
                other_val = other_agent.opinions.get(topic, 0)
                avg_opinions[topic] = (self_val + other_val) / 2
            if self_in_neutral:
                self.opinions = {topic: int(value) for topic, value in avg_opinions.items()}
                logging.info(f"{self} is in the Neutral group, so opinion is updated to the average of {avg_opinions}")
            if other_in_neutral:
                other_agent.opinions = {topic: int(value) for topic, value in avg_opinions.items()}
                logging.info(f"{other_agent} is in the Neutral group, so opinion is updated to the average of {avg_opinions}")
    
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

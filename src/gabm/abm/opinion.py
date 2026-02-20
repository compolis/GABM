"""
Opinion module for GABM.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Standard library imports
import logging
from typing import Dict


class OpinionTopicID:
    """
    A unique identifier for an opinion topic.
    Attributes:
        opinion_topic_id (int): The unique identifier for the opinion topic.
    """
    def __init__(self, opinion_topic_id: int):
        """
        Initialize
        Args:
            opinion_topic_id: The unique identifier for the opinion topic.
        """
        self.id = opinion_topic_id

    def __str__(self):
        """
        Return:
            A string representation.
        """
        return f"OpinionTopicID({self.id})"

    def __repr__(self):
        """
        Return:
            A string representation.
        """
        return self.__str__()   

class OpinionTopic:
    """
    A topic for an opinion.
    Examples:
        id = 0, topic = "positive", description = "A positive opinion."
        id = 1, topic = "neutral", description = "A neutral opinion."
        id = 2, topic = "negative", description = "A negative opinion."
    
    Attributes:
        opinion_topic_id (OpinionTopicID): The unique identifier for the opinion topic.
        topic (str): The topic of the opinion.
        description (str): A description of the opinion topic.
    """
    def __init__(self, opinion_topic_id: OpinionTopicID, topic: str, description: str):
        """
        Initialize
        Args:
            opinion_topic_id: The unique identifier for the opinion topic.
            topic: The topic of the opinion.
            description: A description of the opinion topic.
        """
        self.id = opinion_topic_id
        self.topic = topic
        self.description = description

    def __str__(self):
        """
        Return:
            A string representation.
        """
        return f"OpinionTopic({self.id}, {self.topic})"

    def __repr__(self):
        """
        Return:
            A string representation.
        """
        return self.__str__()

class OpinionValue:
    """
    A value for an opinion.
    Attributes:
        opinion_topic_id (OpinionTopicID): The unique identifier for the opinion.
        value (int): An integer value of the opinion.
         This can be used as a key in a dictionary to map to the description.
         This could be a number mapped to a bipolar Likert scale (https://en.wikipedia.org/wiki/Likert_scale) survey response option.
         It is left to the user to decide how to interpret the value, and what it maps onto.
        description (str): A description of the opinion value.
         For example:
         -2, "Strongly disagree"
         -1, "Disagree"
         0, "Neither agree nor disagree"
         1, "Agree"
         2, "Strongly agree"
    """
    def __init__(self, opinion_topic_id: OpinionTopicID, value: int, description: str):
        """
        Initialize
        Args:
            opinion_topic_id: The unique identifier for the opinion.
            value: An integer value of the opinion.
            description: A description of the opinion value.
        """
        self.opinion_topic_id = opinion_topic_id
        self.value = value
        self.description = description

    def __str__(self):
        """
        Return:
            A string representation.
        """
        return f"OpinionValue({self.opinion_topic_id}, {self.value})"

    def __repr__(self):
        """
        Return:
             A string representation.
        """
        return self.__str__()

class OpinionValues:
    """
    A dictionary of OpinionValues.
    Attributes:
        values (Dict[OpinionTopicID, OpinionValue]): A dictionary mapping OpinionTopicID objects to OpinionValue objects.
    """
    def __init__(self, values: Dict[OpinionTopicID, OpinionValue]):
        """
        Initialize
        Args:
            values: A dictionary mapping OpinionTopicID objects to OpinionValue objects.
        """
        self.values = values
    
    def __str__(self):
        """
        Return:
            A string representation.
        """
        return f"OpinionValues({self.values})"

    def __repr__(self):
        """
        Return:
            A string representation.
        """
        return self.__str__()

class Opinion:
    """
    An Opinion can belong to a Person, OpinionatedGroup, or OpinionatedEnvironment.
    Attributes:
        opinion_id (OpinionTopicID): The unique identifier for the opinion.
        opinion_values (OpinionValues): The opinion values for the opinion.
        value (int): The value of the opinion.
    """
    def __init__(self, opinion_topic_id: OpinionTopicID, opinion_values: OpinionValues, value: int):
        """
        Initialize
        Args:
            opinion_topic_id: The unique identifier for the opinion.
            opinion_values: The opinion values for the opinion.
            value: The value of the opinion.
         The value should be one of the values in the opinion_values, but this is not enforced.
         It is left to the user to ensure that the value is valid for the opinion topic.
         For example, if the opinion topic is "positive", then valid values might be -2, -1, 0, 1, 2, where -2 is "Strongly negative" and 2 is "Strongly positive".
         If an invalid value is set, a warning will be logged, and a ValueError will be raised.
         This allows for flexibility in how opinions are represented and interpreted, while also providing a mechanism for ensuring that values are valid.
         The user can choose to enforce valid values or allow for more flexible representations of opinions.
         The description of the opinion value can be retrieved using the get_description() method, which looks up the description based on the opinion topic ID and value in the opinion_values dictionary.
         If the value is not found in the opinion_values, None will be returned.
         This allows for a clear mapping between numerical values and their corresponding descriptions, which can be useful for interpreting and analyzing opinions in the simulation.
        """
        self.id = opinion_topic_id
        self.opinion_values = opinion_values
        self.value = value

    def __str__(self):
        """
        Return:
            A string representation.
        """
        return f"Opinion({self.id}, {self.value})"

    def __repr__(self):
        """
        Return:
            A string representation.
        """
        return self.__str__()

    def get_description(self) -> str:
        """
        Get the description of the opinion value.
        Returns:
            str: The description of the opinion value, or None if not found.
        """
        if self.opinion_values is not None and self.opinion_id in self.opinion_values.values:
            opinion_value = self.opinion_values.values[self.opinion_id]
            if opinion_value.value == self.value:
                return opinion_value.description
        return None

    def get_value(self) -> int:
        """
        Get the value of the opinion.
        Returns:
            int: The value of the opinion.
        """
        return self.value
    
    def set_value(self, value: int):
        """
        Set the value of the opinion.
        Args:
            value: The new value of the opinion.
        """
        # Check the value is valid
        if self.opinion_values is not None and self.opinion_id in self.opinion_values.values:
            if value not in self.opinion_values.values[self.opinion_id].value:
                message = (f"Value {value} is not a valid value for opinion {self.opinion_id}. "
                           f"Valid values are: {self.opinion_values.values[self.opinion_id].value}")
                logging.warning(message)
                raise ValueError(message)
        self.value = value


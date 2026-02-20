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
        self.id = opinion_topic_id


class OpinionTopic:
    """
    A topic for an opinion.
    Examples:
        id = 0, topic = "positive", description = "A positive opinion."
        id = 1, topic = "neutral", description = "A neutral opinion."
        id = 2, topic = "negative", description = "A negative opinion."
    
    Attributes:
        id (OpinionTopicID): The unique identifier for the opinion topic.
        topic (str): The topic of the opinion.
        description (str): A description of the opinion topic.
    """
    def __init__(self, id: OpinionTopicID, topic: str, description: str, value: int):
        self.opinion_topic_id = opinion_topic_id
        self.topic = topic
        self.description = description

class OpinionValue:
    """
    A value for an opinion.
    Attributes:
        opinion_id (OpinionID): The unique identifier for the opinion.
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
    def __init__(self, opinion_id: OpinionID, value: int, description: str):
        self.opinion_id = opinion_id
        self.value = value
        self.description = description

class OpinionValues:
    """
    A dictionary of OpinionValues.
    Attributes:
        values (Dict[OpinionID, OpinionValue]): A dictionary mapping OpinionID objects to OpinionValue objects.
    """
    def __init__(self, values: Dict[OpinionID, OpinionValue]):
        self.values = values

class Opinion:
    """
    An Opinion can belong to a Person, OpinionatedGroup, or OpinionatedEnvironment.
    Attributes:
        opinion_id (OpinionID): The unique identifier for the opinion.
        opinion_values (OpinionValues): The opinion values for the opinion.
        value (int): The value of the opinion.
    """
    def __init__(self, opinion_id: OpinionID, opinion_values: OpinionValues, value: int):
        """
        Initialize
        """
        self.opinion_id = opinion_id
        self.opinion_values = opinion_values
        self.value = value

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


"""
Interest module for GABM.

For attributing interests to agents, which can influence their behavior and interactions within the simulation.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Standard library imports
import logging
from typing import Dict
# Local imports
from gabm.core.id import GABMID
from gabm.abm.attribute import GABMAttributeID, GABMAttribute, GABMAttributeMap

class InterestTopicID(GABMAttributeID):
    """
    A unique identifier for an interest topic attribute.

    Attributes:
        id (int): The unique identifier for the interest topic.
    """
    def __init__(self, interest_topic_id: int):
        """
        Initialize
        Args:
            interest_topic_id: The unique identifier for the interest topic.
        """
        super().__init__(interest_topic_id)

class InterestTopic():
    """
    A topic for an interest.


    Attributes:
        interest_topic_id (InterestTopicID): The unique identifier for the interest topic.
        topic (str): The topic of the interest.
        description (str): A description of the interest topic.
    
    Examples:
        interest_topic_id = 0, topic = "science", description = "Science interest."
        interest_topic_id = 1, topic = "nature", description = "Nature interest."
        interest_topic_id = 2, topic = "history", description = "History interest."
        interest_topic_id = 3, topic = "music", description = "Music interest."
        interest_topic_id = 4, topic = "sport", description = "Sport interest."
        interest_topic_id = 5, topic = "travel", description = "Travel interest."
        interest_topic_id = 6, topic = "cooking", description = "Cooking interest."
        interest_topic_id = 7, topic = "reading", description = "Reading interest."
        interest_topic_id = 8, topic = "gaming", description = "Gaming interest."
    """

    def __init__(self, interest_topic_id: InterestTopicID, topic: str, description: str):
        """
        Initialize
        Args:
            interest_topic_id: The unique identifier for the interest topic.
            topic: The topic of the interest.
            description: A description of the interest topic.
        """
        self.id = interest_topic_id
        self.topic = topic
        self.description = description

    def __str__(self):
        """
        Return:
            A string representation.
        """
        return f"InterestTopic({self.id}, {self.topic})"

    def __repr__(self):
        """
        Return:
            A string representation.
        """
        return self.__str__()

    @classmethod
    def default_topics(cls) -> Dict[InterestTopicID, "InterestTopic"]:
        """Return the canonical default interest topic catalog."""
        topic_specs = [
            (0, "science", "Science interest."),
            (1, "nature", "Nature interest."),
            (2, "history", "History interest."),
            (3, "music", "Music interest."),
            (4, "sport", "Sport interest."),
            (5, "travel", "Travel interest."),
            (6, "cooking", "Cooking interest."),
            (7, "reading", "Reading interest."),
            (8, "gaming", "Gaming interest."),
        ]
        topics: Dict[InterestTopicID, InterestTopic] = {}
        for topic_id, topic, description in topic_specs:
            interest_topic_id = InterestTopicID(topic_id)
            topics[interest_topic_id] = cls(interest_topic_id, topic, description)
        return topics

    @classmethod
    def default_topic_ids(cls) -> list[InterestTopicID]:
        """Return default topic IDs in deterministic order."""
        return list(cls.default_topics().keys())

class InterestValue():
    """
    A value for an interest.


    Attributes:
        interest_topic_id (InterestTopicID):
            The unique identifier for the interest topic.
        value (int):
            An integer value of the interest. This can be used as a key in a
            dictionary to map to the description. This could be a number mapped to a
            bipolar Likert scale (https://en.wikipedia.org/wiki/Likert_scale) survey
            response option. It is left to the user to decide how to interpret the
            value, and what it maps onto.
        description (str):
            A description of the interest value.
    """

    def __init__(self, interest_topic_id: InterestTopicID, value: int, description: str):
        """
        Initialize
        Args:
            interest_topic_id: The unique identifier for the interest topic.
            value: An integer value of the interest.
            description: A description of the interest value.
        """
        self.interest_topic_id = interest_topic_id
        self.value = value
        self.description = description

    def __str__(self):
        """
        Return:
            A string representation.
        """
        return f"InterestValue({self.interest_topic_id}, {self.value})"

    def __repr__(self):
        """
        Return:
            A string representation.
        """
        return self.__str__()

class InterestValueMap():
    """
    A dictionary of InterestValue objects.

    The key is an InterestTopicID, the value is an InterestValue object.
    
    This can be used to map from an InterestTopicID and value to a description of the interest value.
    For example, if the interest topic is "positive", then valid values might be -2, -1, 0, 1, 2, where -2 is "Strongly negative" and 2 is "Strongly positive".
    The user can choose to enforce valid values or allow for more flexible representations of interests.
    The description of the interest value can be retrieved using the get_description() method, which looks up the description based on the interest topic ID and value in the interest_values dictionary.
    If the value is not found in the interest_values, None will be returned.
    This allows for a clear mapping between numerical values and their corresponding descriptions, which can be useful for interpreting and analyzing interests in the simulation.
    
    Attributes:
        values (Dict[InterestTopicID, InterestValue]): A dictionary mapping InterestTopicID objects to InterestValue objects.
    """

    def __init__(self, values: Dict[InterestTopicID, InterestValue]):
        """
        Initialize
        Args:
            values: A dictionary mapping InterestTopicID objects to InterestValue objects.
        """
        self.values = values
    
    def __str__(self):
        """
        Return:
            A string representation.
        """
        return f"InterestValueMap({self.values})"

    def __repr__(self):
        """
        Return:
            A string representation.
        """
        return self.__str__()

    @classmethod
    def default_for_topic(
        cls,
        interest_topic_id: InterestTopicID,
        value: int = 0,
        description: str = "neutral"
    ) -> "InterestValueMap":
        """
        Build a default single-topic map for simulation setup.

        Args:
            interest_topic_id: Topic to initialize in the map.
            value: Default numeric value for the topic.
            description: Description associated with the default value.

        Returns:
            InterestValueMap with one InterestValue for the given topic.
        """
        default_value = InterestValue(interest_topic_id, value, description)
        return cls({interest_topic_id: default_value})

    @classmethod
    def default_for_topics(
        cls,
        topic_ids: list[InterestTopicID],
        value: int = 0,
        description: str = "neutral"
    ) -> "InterestValueMap":
        """Build default values for multiple topics."""
        values: Dict[InterestTopicID, InterestValue] = {}
        for topic_id in topic_ids:
            values[topic_id] = InterestValue(topic_id, value, description)
        return cls(values)

class Interest():
    """
    An Interest can belong to a Person, InterestGroup, or InterestEnvironment.
    
    Attributes:
        interest_id (InterestTopicID): The unique identifier for the interest.
        interest_values (InterestValueMap): The interest values for the interest.
        value (int): The value of the interest.
    """

    def __init__(self, interest_topic_id: InterestTopicID, interest_values: InterestValueMap, value: int):
        """
        Initialize
        Args:
            interest_topic_id: The unique identifier for the interest.
            interest_values: The interest values for the interest.
            value: The value of the interest.
        """
        self.id = interest_topic_id
        self.interest_values = interest_values
        self.value = value

    def __str__(self):
        """
        Return:
            A string representation.
        """
        return f"Interest({self.id}, {self.value})"

    def __repr__(self):
        """
        Return:
            A string representation.
        """
        return self.__str__()

    def get_description(self) -> str:
        """
        Get the description of the interest value.

        Returns:
            str: The description of the interest value, or None if not found.
        """
        if self.interest_values is not None and self.id in self.interest_values.values:
            interest_value = self.interest_values.values[self.id]
            if interest_value.value == self.value:
                return interest_value.description
        return None

    def get_value(self) -> int:
        """
        Get the value of the interest.

        Returns:
            int: The value of the interest.
        """
        return self.value

    def set_value(self, value: int):
        """
        Set the value of the interest.

        Args:
            value: The new value of the interest.
        """
        # Check the value is valid
        if self.interest_values is not None and self.id in self.interest_values.values:
            if value != self.interest_values.values[self.id].value:
                message = (f"Value {value} is not a valid value for interest {self.id}. "
                           f"Valid values are: {self.interest_values.values[self.id].value}")
                logging.warning(message)
                raise ValueError(message)
        self.value = value
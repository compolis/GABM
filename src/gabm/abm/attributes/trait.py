"""
Trait module for GABM.

For attributing personal traits to agents, which can influence their behavior and interactions within the simulation.

Five personality traits from (https://en.wikipedia.org/wiki/Personality) are:
  Openness to experience
    People high in this tend to be imaginative, insightful, have a broad range of interests, and are curious about the world around them.
  Conscientiousness
    People high in this tend to be thoughtful, have good impulse control, and exhibit goal-directed behaviors. They tend to be organized and mindful of details.
  Extraversion
    People high in this tend to be excitable, sociable, talkative, assertive, and have high amounts of emotional expressiveness. They tend to be outgoing and tend to gain energy in social situations. Being around other people helps them feel energized and excited.
  Agreeableness 
    People high in this tend to be trustworthy, altruistic, kind, and affectionate. They tend to be more cooperative while those low in this trait tend to be more competitive and sometimes manipulative.
  Neuroticism
    People high in this tend to be sad, moody, and emotionally unstable. They tend to experience mood swings, anxiety, irritability, and sadness. Those low in this trait tend to be more stable and emotionally resilient.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Standard library imports
import logging
import random
from typing import Dict
# Local imports
from gabm.core.id import GABMID
from gabm.abm.attribute import GABMAttributeID, GABMAttribute, GABMAttributeMap

class TraitTopicID(GABMAttributeID):
    """
    A unique identifier for a trait topic.

    Attributes:
        id (int): The unique identifier for the trait.
    """
    def __init__(self, trait_id: int):
        """
        Initialize
        Args:
            trait_id: The unique identifier for the trait.
        """
        super().__init__(trait_id)

class TraitTopic():
    """
    A trait topic.

    Attributes:
        trait_topic_id (TraitTopicID): The unique identifier for the trait.
        trait_topic (str): The trait topic.
        description (str): A description of the trait.

    Examples:
        trait_topic_id = 0, trait_topic = "Openness to experience", description = "A trait that features characteristics such as imagination and insight. People high in this trait also tend to have a broad range of interests."
        trait_topic_id = 1, trait_topic = "Conscientiousness", description = "A trait that features high levels of thoughtfulness, good impulse control, and goal-directed behaviors. Those high in conscientiousness tend to be organized and mindful of details."
        trait_topic_id = 2, trait_topic = "Extraversion", description = "A trait that features characteristics such as excitability, sociability, talkativeness, assertiveness, and high amounts of emotional expressiveness. People high in extraversion are outgoing and tend to gain energy in social situations. Being around other people helps them feel energized and excited."
        trait_topic_id = 3, trait_topic = "Agreeableness", description = "A trait that features attributes such as trust, altruism, kindness, affection, and other prosocial behaviors. People high in agreeableness tend to be more cooperative while those low in this trait tend to be more competitive and sometimes manipulative."
        trait_topic_id = 4, trait_topic = "Neuroticism", description = "A trait that features characteristics such as sadness, moodiness, and emotional instability. Individuals high in this trait tend to experience mood swings, anxiety, irritability, and sadness. Those low in this trait tend to be more stable and emotionally resilient."
    """
    def __init__(self, trait_topic_id: TraitTopicID, trait_topic: str, description: str):
        """
        Initialize
        Args:
            trait_topic_id: The unique identifier for the trait topic.
            trait_topic: The trait topic.
            description: A description of the trait.
        """
        self.id = trait_topic_id
        self.trait_topic = trait_topic
        self.description = description

    def __str__(self):
        """
        Return:
            A string representation.
        """
        return f"TraitTopic({self.id}, {self.trait_topic})"

    def __repr__(self):
        """
        Return:
            A string representation.
        """
        return self.__str__()

    @classmethod
    def default_topics(cls) -> Dict[TraitTopicID, "TraitTopic"]:
        """Return the canonical Big Five trait topic catalog."""
        topic_specs = [
            (0, "Openness to experience", "A trait featuring imagination, curiosity, and broad interests."),
            (1, "Conscientiousness", "A trait featuring organization, self-discipline, and goal-directed behavior."),
            (2, "Extraversion", "A trait featuring sociability, assertiveness, and positive emotionality."),
            (3, "Agreeableness", "A trait featuring cooperation, trust, and empathy toward others."),
            (4, "Neuroticism", "A trait featuring emotional instability, anxiety, and mood variability."),
        ]
        topics: Dict[TraitTopicID, TraitTopic] = {}
        for topic_id, topic, description in topic_specs:
            trait_topic_id = TraitTopicID(topic_id)
            topics[trait_topic_id] = cls(trait_topic_id, topic, description)
        return topics

    @classmethod
    def default_topic_ids(cls) -> list[TraitTopicID]:
        """Return default Big Five topic IDs in deterministic order."""
        return list(cls.default_topics().keys())

class TraitValue():
    """
    A value for a trait.

    Attributes:
        trait_topic_id (TraitTopicID):
            The unique identifier for the trait topic.
        value (int):
            An integer value of the trait. This can be used as a key in a
            dictionary to map to the description. This could be a number mapped to a
            bipolar Likert scale (https://en.wikipedia.org/wiki/Likert_scale) survey
            response option. It is left to the user to decide how to interpret the
            value, and what it maps onto.
        description (str):
            A description of the trait value.

    Example::

        -2, "Very low"
        -1, "Low"
         0, "Neither high nor low"
         1, "High"
         2, "Very high"

    """
    def __init__(self, trait_topic_id: TraitTopicID, value: int, description: str):
        """
        Initialize
        Args:
            trait_topic_id: The unique identifier for the trait topic.
            value: An integer value of the trait.
            description: A description of the trait value.
        """
        self.trait_topic_id = trait_topic_id
        self.value = value
        self.description = description

    def __str__(self):
        """
        Return:
            A string representation.
        """
        return f"TraitValue({self.trait_topic_id}, {self.value})"

    def __repr__(self):
        """
        Return:
            A string representation.
        """
        return self.__str__()

class TraitValueMap():
    """
    A dictionary of TraitValue objects.

    The key is a TraitTopicID, the value is a TraitValue object.
    
    This can be used to map from a TraitTopicID and value to a description of the trait value.
    For example, if the trait is "neuroticism", then valid values might be -2, -1, 0, 1, 2, where -2 is "Very low neuroticism" and 2 is "Very high neuroticism".
    The user can choose to enforce valid values or allow for more flexible representations of traits.
    The description of the trait value can be retrieved using the get_description() method, which looks up the description based on the trait ID and value in the trait_values dictionary.
    If the value is not found in the trait_values, None will be returned.
    This allows for a clear mapping between numerical values and their corresponding descriptions, which can be useful for interpreting and analyzing traits in the simulation.
    
    Attributes:
        values (Dict[TraitTopicID, TraitValue]): A dictionary mapping TraitTopicID objects to TraitValue objects.
    """
    def __init__(self, values: Dict[TraitTopicID, TraitValue]):
        """
        Initialize
        Args:
            values: A dictionary mapping TraitTopicID objects to TraitValue objects.
        """
        self.values = values
    
    def __str__(self):
        """
        Return:
            A string representation.
        """
        return f"TraitValueMap({self.values})"

    def __repr__(self):
        """
        Return:
             A string representation.
        """
        return self.__str__()

class TraitValueMap():
    """
    A dictionary of TraitValue objects.

    The key is a TraitTopicID, the value is a TraitValue object.
    
    This can be used to map from a TraitTopicID and value to a description of the trait value.
    For example, if the trait is "neuroticism", then valid values might be -2, -1, 0, 1, 2, where -2 is "Very low neuroticism" and 2 is "Very high neuroticism".
    The user can choose to enforce valid values or allow for more flexible representations of traits.
    The description of the trait value can be retrieved using the get_description() method, which looks up the description based on the trait TopicID and value in the trait_values dictionary.
    If the value is not found in the trait_values, None will be returned.
    This allows for a clear mapping between numerical values and their corresponding descriptions, which can be useful for interpreting and analyzing traits in the simulation.
    
    Attributes:
        values (Dict[TraitTopicID, TraitValue]): A dictionary mapping TraitTopicID objects to TraitValue objects.
    """
    def __init__(self, values: Dict[TraitTopicID, TraitValue]):
        """
        Initialize
        Args:
            values: A dictionary mapping TraitTopic ID objects to TraitValue objects.
        """
        self.values = values
    
    def __str__(self):
        """
        Return:
            A string representation.
        """
        return f"TraitValueMap({self.values})"

    def __repr__(self):
        """
        Return:
            A string representation.
        """
        return self.__str__()

    @classmethod
    def default_for_topic(
        cls,
        trait_topic_id: TraitTopicID,
        value: int = 0,
        description: str = "neither high nor low"
    ) -> "TraitValueMap":
        """Build a default value map for one trait topic."""
        default_value = TraitValue(trait_topic_id, value, description)
        return cls({trait_topic_id: default_value})

    @classmethod
    def default_for_topics(
        cls,
        topic_ids: list[TraitTopicID],
        value: int = 0,
        description: str = "neither high nor low"
    ) -> "TraitValueMap":
        """Build default values for multiple trait topics."""
        values: Dict[TraitTopicID, TraitValue] = {}
        for topic_id in topic_ids:
            values[topic_id] = TraitValue(topic_id, value, description)
        return cls(values)

class Trait():
    """
    A Trait can belong to a Person, TraitGroup, or Environment.

    Attributes:
        trait_topic_id (TraitTopicID): The unique identifier for the trait topic.
        trait_values (TraitValueMap): The trait values for the trait topic.
        value (int): The value of the trait.
    """
    def __init__(self, trait_topic_id: TraitTopicID, trait_values: TraitValueMap, value: int):
        """
        Initialize
        Args:
            trait_topic_id: The unique identifier for the trait topic.
            trait_values: The trait values for the trait topic.
            value: The value of the trait.
        """
        self.id = trait_topic_id
        self.trait_values = trait_values
        self.value = value

    def __str__(self):
        """
        Return:
            A string representation.
        """
        return f"Trait({self.id}, {self.value})"

    def __repr__(self):
        """
        Return:
            A string representation.
        """
        return self.__str__()

    def get_description(self) -> str:
        """
        Get the description of the trait value.

        Returns:
            str: The description of the trait value, or None if not found.
        """
        self.trait_values = trait_values
        self.value = value
        return self.trait_values.values[self.id].description if self.id in self.trait_values.values else None

    def __str__(self):
        """
        Return:
            A string representation.
        """
        return f"Trait({self.id}, {self.value})"

    def __repr__(self):
        """
        Return:
            A string representation.
        """
        return self.__str__()

    def get_description(self) -> str:
        """
        Get the description of the trait value.

        Returns:
            str: The description of the trait value, or None if not found.
        """
        if self.trait_values is not None and self.id in self.trait_values.values:
            trait_value = self.trait_values.values[self.id]
            if trait_value.value == self.value:
                return trait_value.description
        return None

    def get_value(self) -> int:
        """
        Get the value of the trait.

        Returns:
            int: The value of the trait.
        """
        return self.value

    def set_value(self, value: int):
        """
        Set the value of the trait.

        Args:
            value: The new value of the trait.
        """
        self.id = trait_topic_id
        self.trait_values = trait_values
        self.value = value

    def __str__(self):
        """
        Return:
            A string representation.
        """
        return f"Trait({self.id}, {self.value})"

    def __repr__(self):
        """
        Return:
            A string representation.
        """
        return self.__str__()

    def get_description(self) -> str:
        """
        Get the description of the trait value.

        Returns:
            str: The description of the trait value, or None if not found.
        """
        if self.trait_values is not None and self.id in self.trait_values.values:
            trait_value = self.trait_values.values[self.id]
            if trait_value.value == self.value:
                return trait_value.description
        return None

    def get_value(self) -> int:
        """
        Get the value of the trait.

        Returns:
            int: The value of the trait.
        """
        return self.value
    
    def set_value(self, value: int):
        """
        Set the value of the trait.

        Args:
            value: The new value of the trait.
        """
        # Check the value is valid
        if self.trait_values is not None and self.id in self.trait_values.values:
            if value != self.trait_values.values[self.id].value:
                message = (f"Value {value} is not a valid value for trait {self.id}. "
                           f"Valid values are: {self.trait_values.values[self.id].value}")
                logging.warning(message)
                raise ValueError(message)
        self.value = value

    @classmethod
    def random_profile(
        cls,
        seed: int = None,
        topic_ids: list[TraitTopicID] = None,
        value_choices: list[int] = None,
    ) -> Dict[TraitTopicID, "Trait"]:
        """
        Build a random trait profile (default: Big Five topics).

        Args:
            seed: Optional deterministic seed.
            topic_ids: Optional trait topics to generate. Defaults to Big Five.
            value_choices: Optional allowed values. Defaults to [-2, -1, 0, 1, 2].

        Returns:
            Dictionary of TraitTopicID -> Trait.
        """
        rng = random if seed is None else random.Random(seed)
        topic_ids = TraitTopic.default_topic_ids() if topic_ids is None else list(topic_ids)
        value_choices = [-2, -1, 0, 1, 2] if value_choices is None else list(value_choices)

        descriptions = {
            -2: "very low",
            -1: "low",
            0: "neither high nor low",
            1: "high",
            2: "very high",
        }

        traits: Dict[TraitTopicID, Trait] = {}
        for topic_id in topic_ids:
            value = rng.choice(value_choices)
            description = descriptions.get(value, f"value {value}")
            trait_values = TraitValueMap.default_for_topic(topic_id, value=value, description=description)
            traits[topic_id] = cls(topic_id, trait_values, value)
        return traits


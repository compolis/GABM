"""
Values module for GABM.

This module models *human values* as distinct from traits and interests.

Conceptual distinction
----------------------
- Traits: relatively stable dispositional tendencies (e.g., Big Five).
- Interests: topical preferences (e.g., music, reading) that can change quickly.
- Values: guiding life priorities (e.g., family, security, freedom) that shape
  long-term choices and trade-offs.

Research-informed framing
-------------------------
This implementation is guided by cross-cultural values research (notably
Schwartz's theory of basic human values) and practical syntheses indicating
that many populations share a common *set* of values but differ in
*prioritization strength*.

The default topic set is an everyday-language map of common value domains:
1. family and relationships
2. health and wellbeing
3. security and stability
4. freedom and independence
5. achievement and success
6. kindness and helping others
7. belonging and friendship
8. meaning, spirituality, or religion
9. pleasure and enjoyment
10. status, wealth, and influence

Important modeling note
-----------------------
The scoring heuristics below are intentionally lightweight and probabilistic,
intended for simulation initialization rather than deterministic claims about
individuals. They encode broad aggregate tendencies (age, gender, and economic
security effects) while preserving overlap and within-group variation.
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
from gabm.abm.attribute import GABMAttributeID


class ValueTopicID(GABMAttributeID):
    """Unique identifier for a value topic."""

    def __init__(self, value_topic_id: int):
        super().__init__(value_topic_id)


class ValueTopic():
    """A value topic with plain-language label and description."""

    def __init__(self, value_topic_id: ValueTopicID, topic: str, description: str):
        self.id = value_topic_id
        self.topic = topic
        self.description = description

    def __str__(self):
        return f"ValueTopic({self.id}, {self.topic})"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def default_topics(cls) -> Dict[ValueTopicID, "ValueTopic"]:
        """Return the canonical default value topic catalog."""
        topic_specs = [
            (0, "family and relationships", "Prioritizing close family bonds and relational care."),
            (1, "health and wellbeing", "Prioritizing physical and mental wellbeing."),
            (2, "security and stability", "Prioritizing safety, order, and predictable living conditions."),
            (3, "freedom and independence", "Prioritizing autonomy, choice, and self-direction."),
            (4, "achievement and success", "Prioritizing accomplishment, competence, and advancement."),
            (5, "kindness and helping others", "Prioritizing benevolence, fairness, and social welfare."),
            (6, "belonging and friendship", "Prioritizing social connection, friendship, and community."),
            (7, "meaning, spirituality, or religion", "Prioritizing purpose, moral meaning, or spiritual life."),
            (8, "pleasure and enjoyment", "Prioritizing enjoyment, novelty, and quality of life."),
            (9, "status, wealth, and influence", "Prioritizing social status, influence, and material success."),
        ]
        topics: Dict[ValueTopicID, ValueTopic] = {}
        for topic_id, topic, description in topic_specs:
            tid = ValueTopicID(topic_id)
            topics[tid] = cls(tid, topic, description)
        return topics

    @classmethod
    def default_topic_ids(cls) -> list[ValueTopicID]:
        """Return default topic IDs in deterministic order."""
        return list(cls.default_topics().keys())


class ValueStrength():
    """Strength assigned to a value topic."""

    def __init__(self, value_topic_id: ValueTopicID, value: int, description: str):
        self.value_topic_id = value_topic_id
        self.value = value
        self.description = description

    def __str__(self):
        return f"ValueStrength({self.value_topic_id}, {self.value})"

    def __repr__(self):
        return self.__str__()


class ValueStrengthMap():
    """Map from ValueTopicID to ValueStrength."""

    def __init__(self, values: Dict[ValueTopicID, ValueStrength]):
        self.values = values

    def __str__(self):
        return f"ValueStrengthMap({self.values})"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def default_for_topic(
        cls,
        value_topic_id: ValueTopicID,
        value: int = 3,
        description: str = "important",
    ) -> "ValueStrengthMap":
        """Build a default single-topic strength map."""
        strength = ValueStrength(value_topic_id, value, description)
        return cls({value_topic_id: strength})


class Values():
    """
    Value priority for a specific value topic.

    Convention used here is a 1..5 priority scale:
    1 = very low priority, 5 = very high priority.
    """

    def __init__(self, value_topic_id: ValueTopicID, value_strengths: ValueStrengthMap, value: int):
        self.id = value_topic_id
        self.value_strengths = value_strengths
        self.value = value

    def __str__(self):
        return f"Values({self.id}, {self.value})"

    def __repr__(self):
        return self.__str__()

    def get_description(self) -> str:
        """Get mapped description for current value, or None if unmatched."""
        if self.value_strengths is not None and self.id in self.value_strengths.values:
            strength = self.value_strengths.values[self.id]
            if strength.value == self.value:
                return strength.description
        return None

    def get_value(self) -> int:
        return self.value

    def set_value(self, value: int):
        if self.value_strengths is not None and self.id in self.value_strengths.values:
            if value != self.value_strengths.values[self.id].value:
                message = (
                    f"Value {value} is not a valid value for value-topic {self.id}. "
                    f"Valid values are: {self.value_strengths.values[self.id].value}"
                )
                logging.warning(message)
                raise ValueError(message)
        self.value = value

    @staticmethod
    def _value_description(priority: int) -> str:
        mapping = {
            1: "very low priority",
            2: "low priority",
            3: "important",
            4: "very important",
            5: "core priority",
        }
        return mapping.get(priority, f"priority {priority}")

    @classmethod
    def default_profile(
        cls,
        seed: int = None,
        age: int = None,
        gender: str = None,
        economic_security: str = "medium",
        stochastic: bool = True,
    ) -> Dict[ValueTopicID, "Values"]:
        """
        Build a default value-priority profile.

        Heuristic design:
        - Baseline prioritizes family/health/security above status/power.
        - Age shifts from advancement/novelty toward security/care/legacy.
        - Gender applies small overlapping tendency adjustments.
        - Economic security shifts focus between safety/order and self-expression.

        Args:
            seed: Optional deterministic seed.
            age: Optional age in years.
            gender: Optional lower-case string (e.g., "female", "male").
            economic_security: One of "low", "medium", "high".
            stochastic: If True, add small random jitter to preserve variation.
        """
        rng = random if seed is None else random.Random(seed)

        # Baseline rank-informed priorities (1..5).
        # [family, health, security, freedom, achievement, kindness,
        #  belonging, meaning, enjoyment, status]
        scores = {
            ValueTopicID(0): 5,
            ValueTopicID(1): 5,
            ValueTopicID(2): 4,
            ValueTopicID(3): 4,
            ValueTopicID(4): 3,
            ValueTopicID(5): 4,
            ValueTopicID(6): 4,
            ValueTopicID(7): 3,
            ValueTopicID(8): 3,
            ValueTopicID(9): 2,
        }

        # Age effects (broad tendencies, not rules).
        if age is not None:
            if age < 30:
                scores[ValueTopicID(3)] += 1  # freedom
                scores[ValueTopicID(4)] += 1  # achievement
                scores[ValueTopicID(8)] += 1  # enjoyment
                scores[ValueTopicID(2)] -= 1  # security
            elif age >= 60:
                scores[ValueTopicID(2)] += 1  # security
                scores[ValueTopicID(5)] += 1  # kindness
                scores[ValueTopicID(7)] += 1  # meaning
                scores[ValueTopicID(4)] -= 1  # achievement

        # Gender effects (small, overlapping tendencies).
        if gender is not None:
            g = gender.lower().strip()
            if g in {"female", "woman", "f"}:
                scores[ValueTopicID(5)] += 1  # kindness/helping
                scores[ValueTopicID(6)] += 1  # belonging
                scores[ValueTopicID(9)] -= 1  # status/power
            elif g in {"male", "man", "m"}:
                scores[ValueTopicID(4)] += 1  # achievement
                scores[ValueTopicID(9)] += 1  # status/power

        # Economic security effects.
        econ = (economic_security or "medium").lower().strip()
        if econ == "low":
            scores[ValueTopicID(2)] += 1  # security
            scores[ValueTopicID(7)] += 1  # meaning/religion
            scores[ValueTopicID(3)] -= 1  # freedom/self-expression
        elif econ == "high":
            scores[ValueTopicID(3)] += 1  # freedom/self-expression
            scores[ValueTopicID(5)] += 1  # equality/social welfare proxy
            scores[ValueTopicID(2)] -= 1  # security urgency lower

        profile: Dict[ValueTopicID, Values] = {}
        for topic_id in ValueTopic.default_topic_ids():
            base = scores[topic_id]
            if stochastic:
                base += rng.choice([-1, 0, 0, 1])

            priority = max(1, min(5, int(base)))
            description = cls._value_description(priority)
            strength_map = ValueStrengthMap.default_for_topic(topic_id, value=priority, description=description)
            profile[topic_id] = cls(topic_id, strength_map, priority)
        return profile

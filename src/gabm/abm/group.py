# NOTE: This import must be the very first non-empty line in the file (even before docstrings)
# due to Python syntax rules for __future__ imports.
from __future__ import annotations
"""
Group module for GABM.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

from typing import TYPE_CHECKING, Set
if TYPE_CHECKING:
    # Agent is imported under TYPE_CHECKING to avoid circular imports, as Group and Agent reference each other.
    from gabm.abm.agent import Agent

class Group:
    """
    A Group is a collection of Agents that can interact with each other and the environment.
    Attributes:
        id (int): Unique identifier for the group.
        name (str): Optional name for the group.
        members (Set[Agent]): A set of Agent instances that are members of the group.
    """
    def __init__(self, group_id: int, name: str = None):
        """
        Initialize
        """
        self.id = group_id
        self.name = name or str(group_id)
        self.members: Set[Agent] = set()

    def add_member(self, agent: Agent):
        """
        Add agent to the group and update the agent's group membership.
        Args:
            agent: The Agent instance to add to the group.
        """
        self.members.add(agent)
        agent.groups.add(self)

    def remove_member(self, agent: Agent):
        """
        Remove an agent from the group and update the agent's group membership.
        Args:
            agent: The Agent instance to remove from the group.
        """
        self.members.discard(agent)
        agent.groups.discard(self)

    def __str__(self):
        """
        Return:
            String representation.
        """
        return f"Group '{self.name}' (id={self.id}) with {len(self.members)} members"

    def __repr__(self):
        """
        Return:
            Official String representation.
        """
        return self.__str__()

    def list_members(self):
        """
        Return:
            A new tuple of the members.
        """
        return tuple(self.members)

class OpinionatedGroup(Group):
    """
    A Group that has opinions.
    Attributes:
        opinions: A dictionary of opinions. The key is a short name, and the value is an int opinion value. The opinion value may map onto something else.
        (e.g., {"positive": 5}, {"neutral": 0}, {"negative": -3}).
    """
    def __init__(self, group_id: int, name: str = None, opinions: dict = None):
        super().__init__(group_id=group_id, name=name)
        self.opinions = opinions or {}

    def get_AverageOpinion(self, topic: str) -> float:
        """
        Get the average opinion value of the group members on a specific topic.
        Args:
            topic: The topic to get the average opinion on.
        Return:
            The average opinion value for the topic, or None if no members have an opinion on it.
        """
        total_opinion = 0.0
        count = 0
        for member in self.members:
            member_opinion = member.get_Opinion(topic)
            if member_opinion is not None:
                total_opinion += member_opinion
                count += 1
        if count == 0:
            return None
        return total_opinion / count

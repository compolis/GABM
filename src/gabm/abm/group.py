# NOTE: This import must be the very first non-empty line in the file (even before docstrings)
# due to Python syntax rules for __future__ imports.
from __future__ import annotations
"""
Group module for GABM.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.2.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


from typing import TYPE_CHECKING, Set
if TYPE_CHECKING:
    # Agent is imported under TYPE_CHECKING to avoid circular imports, as Group and Agent reference each other.
    from gabm.abm.agent import Agent
from gabm.abm.opinion import OpinionTopicID, OpinionValue, OpinionValues


class GroupID:
    """
    A unique identifier for a Group instance.
    Attributes:
        group_id (int): The unique identifier for the group.
    """
    def __init__(self, group_id: int):
        """
        Initialize
        Args:
            group_id: The unique identifier for the group.
        """
        self.id = group_id

    def __str__(self):
        """
        Return:
            A string representation.
        """
        return f"GroupID({self.id})"

    def __repr__(self):
        """
        Return:
            A string representation.
        """
        return self.__str__()

class Group:
    """
    A Group is a collection of Agents that can interact with each other and the environment.
    Attributes:
        id (GroupID): Unique identifier for the group.
        name (str): Optional name for the group.
        members (Set[Agent]): A set of Agent instances that are members of the group.
    """
    def __init__(self, group_id: GroupID, name: str = None):
        """
        Initialize
        Args:
            group_id: Unique identifier for the Group instance.
            name: Optional name for the group.
        """
        self.id = group_id
        self.name = name or str(group_id)
        self.members: Set[Agent] = set()

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
        opinions: A dictionary of Opinions.
         The keys are OpinionTopicIDs, and the values are Opinion objects.
         This allows the group to have its own opinions, which can be influenced by its members and can also influence its members.
    """
    def __init__(self, group_id: GroupID, name: str = None, opinions: dict = None):
        """
        Initialize
        Args:
            group_id: Unique identifier for the Group instance.
            name: Optional name for the group.
            opinions: A dictionary of opinions, where keys are OpinionTopicIDs and values are Opinion objects.
        """
        super().__init__(group_id=group_id, name=name)
        self.opinions = opinions or {}

    def __str__(self):
        """
        Return:
            String representation.
        """
        super_str = super().__str__()
        return f"{super_str} with opinions: {self.opinions}"

    def __repr__(self):
        """
        Return:
            Official String representation.
        """
        return self.__str__()    

    def get_AverageOpinion(self, opinion_topic_id: OpinionTopicID) -> float:
        """
        Get the average opinion value of the group members on a specific topic.
        Args:
            opinion_topic_id: The opinion topic ID to get the average opinion on.
        Return:
            The average opinion value for the topic, or None if no members have an opinion on it.
        """
        total_opinion = 0.0
        count = 0
        for member in self.members:
            opinion_obj = member.get_opinion(topic)
            if opinion_obj is not None and hasattr(opinion_obj, 'value'):
                total_opinion += opinion_obj.value
                count += 1
        if count == 0:
            return None
        return total_opinion / count

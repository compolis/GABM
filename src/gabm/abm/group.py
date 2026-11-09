# NOTE: This import must be the very first non-empty line in the file (even before docstrings)
# due to Python syntax rules for __future__ imports.
from __future__ import annotations
"""
Group module for GABM.

For representing a collection of Agents that can interact with each other and the environment. The Group class is a base class for more specific group types, such as OpinionGroup.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.2.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


from typing import TYPE_CHECKING, Set
# Local imports
from gabm.core.id import GABMID
if TYPE_CHECKING:
    # Agent is imported under TYPE_CHECKING to avoid circular imports, as Group and Agent reference each other.
    from gabm.abm.agent import Agent
from gabm.abm.attributes.opinion import OpinionTopicID, OpinionValue, OpinionValueMap
from gabm.abm.attributes.interest import InterestTopicID, InterestValue, InterestValueMap, Interest
from gabm.abm.attributes.trait import TraitTopicID, TraitValue, TraitValueMap, Trait

class GroupID(GABMID):
    """
    A unique identifier for a Group instance.

    Attributes:
        group_id (int): The unique identifier for the group.
    """
    def __init__(self, group_id: int):
        super().__init__(group_id)

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

class InterestGroup(Group):
    """
    A Group that has shared interests.
    
    Attributes:
        interests: A dictionary of Interests.
         The keys are InterestTopicIDs, and the values are Interest objects.
         This allows the group to have its own interests, which can be influenced by its members and can also influence its members.
    """
    def __init__(self, group_id: GroupID, name: str = None, interests: dict = None):
        """
        Initialize
        Args:
            group_id: Unique identifier for the Group instance.
            name: Optional name for the group.
            interests: A dictionary of interests, where keys are InterestTopicIDs and values are Interest objects.
        """
        super().__init__(group_id=group_id, name=name)
        self.interests = interests or {}

    def __str__(self):
        """
        Return:
            String representation.
        """
        super_str = super().__str__()
        return f"{super_str} with interests: {self.interests}"

    def __repr__(self):
        """
        Return:
            Official String representation.
        """
        return self.__str__()

    def get_AverageInterest(self, interest_topic_id: InterestTopicID) -> float:
        """
        Get the average interest value of the group members on a specific topic.

        Args:
            interest_topic_id: The interest topic ID to get the average interest on.

        Returns:
            The average interest value for the topic, or None if no members have an interest on it.

        """
        total_interest = 0.0
        count = 0
        for member in self.members:
            interest_obj = member.get_interest(interest_topic_id)
            if interest_obj is not None and hasattr(interest_obj, 'value'):
                total_interest += interest_obj.value
                count += 1
        if count == 0:
            return None
        return total_interest / count

class OpinionGroup(Group):
    """
    A Group that has shared opinion.
    
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

        Returns:
            The average opinion value for the topic, or None if no members have an opinion on it.

        """
        total_opinion = 0.0
        count = 0
        for member in self.members:
            opinion_obj = member.get_opinion(opinion_topic_id)
            if opinion_obj is not None and hasattr(opinion_obj, 'value'):
                total_opinion += opinion_obj.value
                count += 1
        if count == 0:
            return None
        return total_opinion / count

class TraitGroup(Group):
    """
    A Group that has shared traits.
    
    Attributes:
        traits: A dictionary of Traits.
         The keys are TraitTopicIDs, and the values are Trait objects.
         This allows the group to have its own traits, which can be influenced by its members and can also influence its members.
    """
    def __init__(self, group_id: GroupID, name: str = None, traits: dict = None):
        """
        Initialize
        Args:
            group_id: Unique identifier for the Group instance.
            name: Optional name for the group.
            traits: A dictionary of traits, where keys are TraitTopicIDs and values are Trait objects.
        """
        super().__init__(group_id=group_id, name=name)
        self.traits = traits or {}

    def __str__(self):
        """
        Return:
            String representation.
        """
        super_str = super().__str__()
        return f"{super_str} with traits: {self.traits}"

    def __repr__(self):
        """
        Return:
            Official String representation.
        """
        return self.__str__()
    
    def get_AverageTrait(self, trait_topic_id: TraitTopicID) -> float:
        """
        Get the average trait value of the group members on a specific topic.

        Args:
            trait_topic_id: The trait topic ID to get the average trait on.

        Returns:
            The average trait value for the topic, or None if no members have a trait on it.

        """
        total_trait = 0.0
        count = 0
        for member in self.members:
            trait_obj = member.get_trait(trait_topic_id)
            if trait_obj is not None and hasattr(trait_obj, 'value'):
                total_trait += trait_obj.value
                count += 1
        if count == 0:
            return None
        return total_trait / count
# NOTE: This import must be the very first non-empty line in the file (even before docstrings)
# due to Python syntax rules for __future__ imports.
from __future__ import annotations
"""
Defines the Group class for collections of Agent instances.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

from typing import TYPE_CHECKING, Set
if TYPE_CHECKING:
    from gabm.abm.agents.agent import Agent

class Group:
    def __init__(self, group_id: int, name: str = None):
        """
        Initialize a group with an id, name, and empty set of members.
        Args:
            group_id: The uniqueinteger id of the group.
            name: Optional name for the group (defaults to str(group_id)).
        """
        self.id = group_id
        self.name = name or str(group_id)
        self.members: Set[Agent] = set()

    def add_member(self, agent: Agent):
        """
        Add an agent to the group and update the agent's group membership.
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
        return f"Group '{self.name}' (id={self.id}) with {len(self.members)} members"

    def list_members(self):
        """
        Return a list of the group's members.
        """
        return list(self.members)

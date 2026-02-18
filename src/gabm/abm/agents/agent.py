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

# To avoid circular imports, TYPE_CHECKING is used to import Environment only for type hints.
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gabm.abm.environment import Environment

from typing import Set
import logging
if TYPE_CHECKING:
    from gabm.abm.agents.group import Group

class Agent:
    def __init__(self, agent_id: int, environment: 'Environment', opinion: float = 0.0):
        """
        Initialize an agent.
        Args:
            agent_id: The unique integer id of the agent.
            environment: The shared environment.
            opinion: A float representing the agent's opinion on a topic (for demonstration purposes).
        """
        self.id = agent_id
        self.environment = environment
        self.opinion = opinion
        self.groups: Set['Group'] = set()

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

    def __str__(self):
        """
        String representation of the agent, showing its index.
        """
        return f"Agent (id={self.id})"

    def communicate(self, i: int):
        """
        Communicate with another agent.
        Args:
            i: The index of the agent to communicate with.
        """
        other_agent = self.environment.agents_active[i]
        logging.info(f"{self} is communicating with {other_agent}")
        # If either agent is in the Neutral group, both update their opinions to the average
        neutral_groups = [group for group in self.environment.groups_active.values() if group.name == "Neutral"]
        self_in_neutral = any(self in group.members for group in neutral_groups)
        other_in_neutral = any(other_agent in group.members for group in neutral_groups)
        if self_in_neutral or other_in_neutral:
            avg_opinion = (self.opinion + other_agent.opinion) / 2
            if self_in_neutral:
                self.opinion = avg_opinion
                logging.info(f"{self} is in the Neutral group, so opinion is updated to the average of {avg_opinion:.2f}")
            if other_in_neutral:
                other_agent.opinion = avg_opinion
                logging.info(f"{other_agent} is in the Neutral group, so opinion is updated to the average of {avg_opinion:.2f}")
        logging.info(f"{self} has opinion {self.opinion:.2f} after communicating with {other_agent}")
        
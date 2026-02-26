"""
ID module for GABM.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import logging

# Generic base class for all ID types
class GABMID:
    def __init__(self, id_value: int):
        """
        Initialize
        Args:
            id_value (int): The unique identifier value.
        """
        self.id = id_value

    def __str__(self):
        """
        Return:
            A string representation.
        """
        return f"{self.__class__.__name__}({self.id})"

    def __repr__(self):
        """
        Return:
            A string representation.
        """
        return self.__str__()

    def __eq__(self, other):
        """
        Return:
            True if the other object is of the same class and has the same ID, False otherwise.
        """
        return isinstance(other, self.__class__) and self.id == other.id

    def __hash__(self):
        """
        Return:
            The hash of the ID value.
        """
        return hash(self.id)
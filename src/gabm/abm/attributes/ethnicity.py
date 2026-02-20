"""
Ethnicity module for GABM.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Standard library imports
import logging
from typing import Dict


class EthnicityID():
    """
    A unique identifier for an Ethnicity instance.
    Attributes:
        ethnicity_id (int): The unique identifier for the ethnicity.
    """
    def __init__(self, ethnicity_id: int):
        self.id = ethnicity_id

    def __str__(self):
        """
        Return:
            A string representation.
        """
        return f"EthnicityID({self.id})"

    def __repr__(self):
        """
        Return:
            A string representation.
        """
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, EthnicityID):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)


class Ethnicity():
    """
    An Ethnicity.
    Attributes:
        id (EthnicityID): Unique identifier for the ethnicity.
        value (int): The value of the ethnicity.
        description (str): The description of the ethnicity.
    """
    def __init__(self, ethnicity_id: EthnicityID, value: int, description: str):
        """
        Initialize
        Args:
            ethnicity_id (EthnicityID): The unique identifier for the ethnicity.
            value (int): The value of the ethnicity.
            description (str): The description of the ethnicity.
        """
        self.id = ethnicity_id
        self.value = value
        self.description = description

    def __str__(self):
        """
        Return:
            A string representation.
        """
        return self.description

    def __repr__(self):
        """
        Return:
            A string representation.
        """
        return self.__str__()

class EthnicityMap():
    """
    A mapping of EthnicityIds to Ethnicity.
    The mapping can be extended to include more ethnicities as needed.
    Attributes:
        ethnicity_map (dict): A dictionary mapping EthnicityIds to Ethnicity objects.
            The keys are EthnicityIds, and the values are Ethnicity objects.
            The default mapping includes:
                0: "white",
                1: "asian",
                2: "black".
                3: "mixed",
                4: "other".
    """
    def __init__(self):
        """
        Initialize the Ethnicities object.
        """
        e0 = EthnicityID(0)
        e1 = EthnicityID(1)
        e2 = EthnicityID(2)
        e3 = EthnicityID(3)
        e4 = EthnicityID(4)
        self.ethnicity_map = {
            e0: Ethnicity(e0, 0, "white"),
            e1: Ethnicity(e1, 1, "asian"),
            e2: Ethnicity(e2, 2, "black"),
            e3: Ethnicity(e3, 3, "mixed"),
            e4: Ethnicity(e4, 4, "other")
        }

    def __str__(self):
        """
        Return:
            The string representation.
        """
        return f"Ethnicities({self.ethnicity_map})"

    def __repr__(self):
        """
        Return:
            Official string representation.
        """
        return self.__str__()
    
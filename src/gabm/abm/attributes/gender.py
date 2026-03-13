"""
Gender module for GABM.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.4.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Standard library imports
import logging
from typing import Dict
# Local imports
from gabm.core.id import GABMID
from gabm.abm.attribute import GABMAttributeID, GABMAttribute, GABMAttributeMap

class GenderID(GABMAttributeID):
    """
    A unique identifier for a Gender attribute.

    Attributes:
        id (int): The unique identifier for the gender.
    """
    def __init__(self, gender_id: int):
        """
        Initialize
        Args:
            gender_id (int): The unique identifier for the gender.
        """
        super().__init__(gender_id)

# Standard GenderID constants for clarity and maintainability
GenderID.UNKNOWN = GenderID(0)  # type: GenderID
GenderID.FEMALE = GenderID(1)   # type: GenderID
GenderID.MALE = GenderID(2)     # type: GenderID
GenderID.NON_BINARY = GenderID(3)  # type: GenderID

class Gender(GABMAttribute):
    """
    A Gender.

    Attributes:
        id (GenderID): Unique identifier for the gender.
        description (str): The description of the gender.
    """
    def __init__(self, gender_id: GenderID, description: str):
        """
        Initialize
        Args:
            gender_id (GenderID): The unique identifier for the gender.
            description (str): The description of the gender.
        """
        super().__init__(gender_id, description)

class GenderMap(GABMAttributeMap):
    """
    A mapping of GenderIds to Genders.

    By default, the map is initialized as follows::

        items: Dict[GenderID, Gender] = {
            GenderID.UNKNOWN: Gender(GenderID.UNKNOWN, "unknown"),
            GenderID.FEMALE: Gender(GenderID.FEMALE, "female"),
            GenderID.MALE: Gender(GenderID.MALE, "male"),
            GenderID.NON_BINARY: Gender(GenderID.NON_BINARY, "non-binary"),
        }
        super().__init__(items)
    """
    def __init__(self):
        """
        Initialize the GenderMap object.
        """
        items: Dict[GenderID, Gender] = {
            GenderID.UNKNOWN: Gender(GenderID.UNKNOWN, "unknown"),
            GenderID.FEMALE: Gender(GenderID.FEMALE, "female"),
            GenderID.MALE: Gender(GenderID.MALE, "male"),
            GenderID.NON_BINARY: Gender(GenderID.NON_BINARY, "non-binary"),
        }
        super().__init__(items)
    
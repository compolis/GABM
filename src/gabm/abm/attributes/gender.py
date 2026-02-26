"""
Gender module for GABM.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.3.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Standard library imports
import logging
from typing import Dict
# Local imports
from gabm.core.id import GABMID
from gabm.abm.attribute import GABMAttribute, GABMAttributeMap

class GenderID(GABMID):
    """
    A unique identifier for a Gender instance.
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
    By default, the map is initialized as follows:
        g0 = GenderID(0)
        g1 = GenderID(1)
        g2 = GenderID(2)
        g3 = GenderID(3)
        items: Dict[GenderID, Gender] = {
            g0: Gender(g0, "unknown"),
            g1: Gender(g1, "female"),
            g2: Gender(g2, "male"),
            g3: Gender(g3, "non-binary"),
        }
        super().__init__(items)
    """
    def __init__(self):
        """
        Initialize the GenderMap object.
        """
        g0 = GenderID(0)
        g1 = GenderID(1)
        g2 = GenderID(2)
        g3 = GenderID(3)
        items: Dict[GenderID, Gender] = {
            g0: Gender(g0, "unknown"),
            g1: Gender(g1, "female"),
            g2: Gender(g2, "male"),
            g3: Gender(g3, "non-binary"),
        }
        super().__init__(items)
    
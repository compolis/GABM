"""
Family module for GABM.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Standard library imports
import logging
from typing import Dict
# Local imports
from gabm.core.id import GABMID
from gabm.abm.attribute import GABMAttribute, GABMAttributeMap

class FamilyID(GABMID):
    """
    A unique identifier for a Family instance.

    Attributes:
        id (int): The unique identifier for the family.
    """
    def __init__(self, family_id: int):
        """
        Initialize
        Args:
            family_id (int): The unique identifier for the family.
        """
        super().__init__(family_id)

# Standard FamilyID constants for clarity and maintainability
FamilyID.UNKNOWN = FamilyID(0)  # type: FamilyID
FamilyID.NOT_MARRIED = FamilyID(1)  # type: FamilyID
FamilyID.MARRIED = FamilyID(2)  # type: FamilyID

class Family(GABMAttribute):
    """
    A Family.

    Attributes:
        id (FamilyID): Unique identifier for the family.
        description (str): The description of the family.
    """
    def __init__(self, family_id: FamilyID, description: str):
        """
        Initialize
        Args:
            family_id (FamilyID): The unique identifier for the family.
            description (str): The description of the family.
        """
        super().__init__(family_id, description)

class FamilyMap(GABMAttributeMap):
    """
    A mapping of FamilyIds to Families.

    By default, the map is initialized as follows::

        items: Dict[FamilyID, Family] = {
            FamilyID.UNKNOWN: Family(FamilyID.UNKNOWN, "unknown"),
            FamilyID.NOT_MARRIED: Family(FamilyID.NOT_MARRIED, "not married"),
            FamilyID.MARRIED: Family(FamilyID.MARRIED, "married"),
        }
        super().__init__(items)
    """
    def __init__(self):
        """
        Initialize the FamilyMap object.
        """
        items: Dict[FamilyID, Family] = {
            FamilyID.UNKNOWN: Family(FamilyID.UNKNOWN, "unknown"),
            FamilyID.NOT_MARRIED: Family(FamilyID.NOT_MARRIED, "not married"),
            FamilyID.MARRIED: Family(FamilyID.MARRIED, "married"),
        }
        super().__init__(items)
    
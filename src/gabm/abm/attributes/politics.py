"""
Politics module for GABM.
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
from gabm.abm.attribute import GABMAttributeID, GABMAttribute, GABMAttributeMap

class PoliticsID(GABMAttributeID):
    """
    A unique identifier for a Politics attribute.

    Attributes:
        id (int): The unique identifier for the politics attribute.
    """
    def __init__(self, politics_id: int):
        """
        Initialize
        Args:
            politics_id (int): The unique identifier for the politics attribute.
        """
        super().__init__(politics_id)

# Standard PoliticsID constants for clarity and maintainability
PoliticsID.UNKNOWN = PoliticsID(0)
PoliticsID.FAR_LEFT = PoliticsID(1)
PoliticsID.LEFT = PoliticsID(2)
PoliticsID.CENTRE = PoliticsID(3)
PoliticsID.RIGHT = PoliticsID(4)
PoliticsID.FAR_RIGHT = PoliticsID(5)

class Politics(GABMAttribute):
    """
    For representing politics.

    Attributes:
        id (PoliticsID): Unique identifier for the politics.
        description (str): The description of the politics.
    """
    def __init__(self, politics_id: PoliticsID, description: str):
        """
        Initialize
        Args:
            politics_id (PoliticsID): The unique identifier for the politics.
            description (str): The description of the politics.
        """
        super().__init__(politics_id, description)

class PoliticsMap(GABMAttributeMap):
    """
    A mapping of PoliticsIds to Politics.

    By default, the map is initialized as follows::

        items: Dict[PoliticsID, Politics] = {
            PoliticsID.UNKNOWN: Politics(PoliticsID.UNKNOWN, "unknown"),
            PoliticsID.FAR_LEFT: Politics(PoliticsID.FAR_LEFT, "far left"),
            PoliticsID.LEFT: Politics(PoliticsID.LEFT, "left"),
            PoliticsID.CENTRE: Politics(PoliticsID.CENTRE, "centre"),
            PoliticsID.RIGHT: Politics(PoliticsID.RIGHT, "right"),
            PoliticsID.FAR_RIGHT: Politics(PoliticsID.FAR_RIGHT, "far right")
        }
        super().__init__(items)
    """
    def __init__(self):
        items: Dict[PoliticsID, Politics] = {
            PoliticsID.UNKNOWN: Politics(PoliticsID.UNKNOWN, "unknown"),
            PoliticsID.FAR_LEFT: Politics(PoliticsID.FAR_LEFT, "far left"),
            PoliticsID.LEFT: Politics(PoliticsID.LEFT, "left"),
            PoliticsID.CENTRE: Politics(PoliticsID.CENTRE, "centre"),
            PoliticsID.RIGHT: Politics(PoliticsID.RIGHT, "right"),
            PoliticsID.FAR_RIGHT: Politics(PoliticsID.FAR_RIGHT, "far right")
        }
        super().__init__(items)
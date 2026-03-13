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
# Local imports
from gabm.core.id import GABMID
from gabm.abm.attribute import GABMAttributeID, GABMAttribute, GABMAttributeMap

class RegionID(GABMAttributeID):
    """
    A unique identifier for a Region attribute.

    Attributes:
        id (int): The unique identifier for the region attribute.
    """
    def __init__(self, region_id: int):
        """
        Initialize
        Args:
            region_id (int): The unique identifier for the region attribute.
        """
        super().__init__(region_id)

# Standard RegionID constants for clarity and maintainability
RegionID.UNKNOWN = RegionID(0)
RegionID.NORTH_WEST = RegionID(1)
RegionID.NORTH = RegionID(2)
RegionID.NORTH_EAST = RegionID(3)
RegionID.WEST = RegionID(4)
RegionID.CENTRAL = RegionID(5)
RegionID.EAST = RegionID(6)
RegionID.SOUTH_WEST = RegionID(7)
RegionID.SOUTH = RegionID(8)
RegionID.SOUTH_EAST = RegionID(9)

class Region(GABMAttribute):
    """
    A Region.

    Attributes:
        id (RegionID): Unique identifier for the region.
        description (str): The description of the region.
    """
    def __init__(self, region_id: RegionID, description: str):
        """
        Initialize
        Args:
            region_id (RegionID): The unique identifier for the region.
            description (str): The description of the region.
        """
        super().__init__(region_id, description)

class RegionMap(GABMAttributeMap):
    """
    A mapping of RegionIds to Region.

    By default, the map is initialized as follows::

        items: Dict[RegionID, Region] = {
            RegionID.UNKNOWN: Region(RegionID.UNKNOWN, "unknown"),
            RegionID.NORTH_WEST: Region(RegionID.NORTH_WEST, "north-west"),
            RegionID.NORTH: Region(RegionID.NORTH, "north"),
            RegionID.NORTH_EAST: Region(RegionID.NORTH_EAST, "north-east"),
            RegionID.WEST: Region(RegionID.WEST, "west"),
            RegionID.CENTRAL: Region(RegionID.CENTRAL, "central"),
            RegionID.EAST: Region(RegionID.EAST, "east"),
            RegionID.SOUTH_WEST: Region(RegionID.SOUTH_WEST, "south-west"),
            RegionID.SOUTH: Region(RegionID.SOUTH, "south"),
            RegionID.SOUTH_EAST: Region(RegionID.SOUTH_EAST, "south-east")
        }
        super().__init__(items)
    """
    def __init__(self):
        """
        Initialize the Regions object.
        """
        items: Dict[RegionID, Region] = {
            RegionID.UNKNOWN: Region(RegionID.UNKNOWN, "unknown"),
            RegionID.NORTH_WEST: Region(RegionID.NORTH_WEST, "north-west"),
            RegionID.NORTH: Region(RegionID.NORTH, "north"),
            RegionID.NORTH_EAST: Region(RegionID.NORTH_EAST, "north-east"),
            RegionID.WEST: Region(RegionID.WEST, "west"),
            RegionID.CENTRAL: Region(RegionID.CENTRAL, "central"),
            RegionID.EAST: Region(RegionID.EAST, "east"),
            RegionID.SOUTH_WEST: Region(RegionID.SOUTH_WEST, "south-west"),
            RegionID.SOUTH: Region(RegionID.SOUTH, "south"),
            RegionID.SOUTH_EAST: Region(RegionID.SOUTH_EAST, "south-east")
        }
        super().__init__(items)
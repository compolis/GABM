"""
Wealth module for GABM.
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

class WealthID(GABMAttributeID):
    """
    A unique identifier for a Wealth attribute.

    Attributes:
        wealth_id (int): The unique identifier for the wealth attribute.
    """
    def __init__(self, wealth_id: int):
        """
        Initialize the WealthID object.

        Args:
            wealth_id (int): The unique identifier for the wealth attribute.
        """
        super().__init__(wealth_id)

# Standard WealthID constants for clarity and maintainability
WealthID.UNKNOWN = WealthID(0)
WealthID.NEGATIVE = WealthID(1)
WealthID.ZERO_TO_Q1 = WealthID(2)
WealthID.Q1_TO_MEDIAN = WealthID(3)
WealthID.MEDIAN_TO_Q3 = WealthID(4)
WealthID.Q3_TO_TOP_10 = WealthID(5)
WealthID.TOP_10_TO_TOP_1 = WealthID(6)
WealthID.TOP_1_TO_TOP_0_1 = WealthID(7)
WealthID.TOP_0_1_TO_TOP_0_01 = WealthID(8)
WealthID.TOP_0_01_TO_TOP_0_001 = WealthID(9)
WealthID.TOP_0_001 = WealthID(10)

class Wealth(GABMAttribute):
    """
    For representing wealth.

    Attributes:
        id (WealthID): Unique identifier for the wealth.
        description (str): The description of the wealth.
    """
    def __init__(self, wealth_id: WealthID, description: str):
        """
        Initialize
        Args:
            wealth_id (WealthID): The unique identifier for the wealth.
            description (str): The description of the wealth.
        """
        self.id = wealth_id
        self.description = description

class WealthMap(GABMAttributeMap):
    """
    A mapping of WealthIds to Wealth.

    By default, the map is initialized as follows::

        self.wealth_map: Dict[WealthID, Wealth] = {
            WealthID.UNKNOWN: Wealth(WealthID.UNKNOWN, "unknown"),
            WealthID.NEGATIVE: Wealth(WealthID.NEGATIVE, "negative"),
            WealthID.ZERO_TO_Q1: Wealth(WealthID.ZERO_TO_Q1, "zero to q1"),
            WealthID.Q1_TO_MEDIAN: Wealth(WealthID.Q1_TO_MEDIAN, "q1 to median"),
            WealthID.MEDIAN_TO_Q3: Wealth(WealthID.MEDIAN_TO_Q3, "median to q3"),
            WealthID.Q3_TO_TOP_10: Wealth(WealthID.Q3_TO_TOP_10, "q3 to top 10%"),
            WealthID.TOP_10_TO_TOP_1: Wealth(WealthID.TOP_10_TO_TOP_1, "top 10% to top 1%"),
            WealthID.TOP_1_TO_TOP_0_1: Wealth(WealthID.TOP_1_TO_TOP_0_1, "top 1% to top 0.1%"),
            WealthID.TOP_0_1_TO_TOP_0_01: Wealth(WealthID.TOP_0_1_TO_TOP_0_01, "top 0.1% to top 0.01%"),
            WealthID.TOP_0_01_TO_TOP_0_001: Wealth(WealthID.TOP_0_01_TO_TOP_0_001, "top 0.01% to top 0.001%"),
            WealthID.TOP_0_001: Wealth(WealthID.TOP_0_001, "top 0.001%")
        }
    """
    def __init__(self):
        """
        Initialize the WealthMap object.
        """
        self.wealth_map: Dict[WealthID, Wealth] = {
            WealthID.UNKNOWN: Wealth(WealthID.UNKNOWN, "unknown"),
            WealthID.NEGATIVE: Wealth(WealthID.NEGATIVE, "negative"),
            WealthID.ZERO_TO_Q1: Wealth(WealthID.ZERO_TO_Q1, "zero to q1"),
            WealthID.Q1_TO_MEDIAN: Wealth(WealthID.Q1_TO_MEDIAN, "q1 to median"),
            WealthID.MEDIAN_TO_Q3: Wealth(WealthID.MEDIAN_TO_Q3, "median to q3"),
            WealthID.Q3_TO_TOP_10: Wealth(WealthID.Q3_TO_TOP_10, "q3 to top 10%"),
            WealthID.TOP_10_TO_TOP_1: Wealth(WealthID.TOP_10_TO_TOP_1, "top 10% to top 1%"),
            WealthID.TOP_1_TO_TOP_0_1: Wealth(WealthID.TOP_1_TO_TOP_0_1, "top 1% to top 0.1%"),
            WealthID.TOP_0_1_TO_TOP_0_01: Wealth(WealthID.TOP_0_1_TO_TOP_0_01, "top 0.1% to top 0.01%"),
            WealthID.TOP_0_01_TO_TOP_0_001: Wealth(WealthID.TOP_0_01_TO_TOP_0_001, "top 0.01% to top 0.001%"),
            WealthID.TOP_0_001: Wealth(WealthID.TOP_0_001, "top 0.001%")
        }
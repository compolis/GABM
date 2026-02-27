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
from gabm.abm.attribute import GABMAttribute, GABMAttributeMap

class WealthID(GABMID):
    """
    A unique identifier for a Wealth instance.
    Attributes:
        wealth_id (int): The unique identifier for the wealth.
    """
    def __init__(self, wealth_id: int):
        super().__init__(wealth_id)

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
    By default, the map is initialized as follows:
        w0 = WealthID(0)
        w1 = WealthID(1)
        w2 = WealthID(2)
        w3 = WealthID(3)
        w4 = WealthID(4)
        w5 = WealthID(5)
        w6 = WealthID(6)
        w7 = WealthID(7)
        w8 = WealthID(8)
        w9 = WealthID(9)
        w10 = WealthID(10)
        self.wealth_map: Dict[WealthID, Wealth] = {
            w0: Wealth(w0, "unknown"),
            w1: Wealth(w1, "negative"),
            w2: Wealth(w2, "zero to q1"),
            w3: Wealth(w3, "q1 to median"),
            w4: Wealth(w4, "median to q3"),
            w5: Wealth(w5, "q3 to top 10%"),
            w6: Wealth(w6, "top 10% to top 1%"),
            w7: Wealth(w7, "top 1% to top 0.1%"),
            w8: Wealth(w8, "top 0.1% to top 0.01%"),
            w9: Wealth(w9, "top 0.01% to top 0.001%"),
            w10: Wealth(w10, "top 0.001%")
        }
    """
    def __init__(self):
        """
        Initialize the WealthMap object.
        """
        w0 = WealthID(0)
        w1 = WealthID(1)
        w2 = WealthID(2)
        w3 = WealthID(3)
        w4 = WealthID(4)
        w5 = WealthID(5)
        w6 = WealthID(6)
        w7 = WealthID(7)
        w8 = WealthID(8)
        w9 = WealthID(9)
        w10 = WealthID(10)
        self.wealth_map: Dict[WealthID, Wealth] = {
            w0: Wealth(w0, "unknown"),
            w1: Wealth(w1, "negative"),
            w2: Wealth(w2, "zero to q1"),
            w3: Wealth(w3, "q1 to median"),
            w4: Wealth(w4, "median to q3"),
            w5: Wealth(w5, "q3 to top 10%"),
            w6: Wealth(w6, "top 10% to top 1%"),
            w7: Wealth(w7, "top 1% to top 0.1%"),
            w8: Wealth(w8, "top 0.1% to top 0.01%"),
            w9: Wealth(w9, "top 0.01% to top 0.001%"),
            w10: Wealth(w10, "top 0.001%")
        }
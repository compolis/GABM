"""
Income module for GABM.
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

class IncomeID(GABMAttributeID):
    """
    A unique identifier for an Income attribute.

    Attributes:
        id (int): The unique identifier for the income.
    """
    def __init__(self, income_id: int):
        """
        Initialize
        Args:
            income_id (int): The unique identifier for the income.
        """
        super().__init__(income_id)

# Standard IncomeID constants for clarity and maintainability
IncomeID.UNKNOWN = IncomeID(0)
IncomeID.ZERO_TO_Q1 = IncomeID(1)
IncomeID.Q1_TO_MEDIAN = IncomeID(2)
IncomeID.MEDIAN_TO_Q3 = IncomeID(3)
IncomeID.Q3_TO_TOP_10 = IncomeID(4)
IncomeID.TOP_10_TO_TOP_1 = IncomeID(5)
IncomeID.TOP_1_TO_TOP_0_1 = IncomeID(6)
IncomeID.TOP_0_1_TO_TOP_0_01 = IncomeID(7)
IncomeID.TOP_0_01_TO_TOP_0_001 = IncomeID(8)
IncomeID.TOP_0_001 = IncomeID(9)

class Income(GABMAttribute):
    """
    For representing income.

    Attributes:
        id (IncomeID): Unique identifier for the income.
        description (str): The description of the income.
    """
    def __init__(self, income_id: IncomeID, description: str):
        """
        Initialize
        Args:
            income_id (IncomeID): The unique identifier for the income.
            description (str): The description of the income.
        """
        super().__init__(income_id, description)

class IncomeMap(GABMAttributeMap):
    """
    A mapping of IncomeIds to Income.

    By default, the map is initialized as follows::

        items: Dict[IncomeID, Income] = {
            IncomeID.UNKNOWN: Income(IncomeID.UNKNOWN, "unknown"),
            IncomeID.ZERO_TO_Q1: Income(IncomeID.ZERO_TO_Q1, "zero to q1"),
            IncomeID.Q1_TO_MEDIAN: Income(IncomeID.Q1_TO_MEDIAN, "q1 to median"),
            IncomeID.MEDIAN_TO_Q3: Income(IncomeID.MEDIAN_TO_Q3, "median to q3"),
            IncomeID.Q3_TO_TOP_10: Income(IncomeID.Q3_TO_TOP_10, "q3 to top 10%"),
            IncomeID.TOP_10_TO_TOP_1: Income(IncomeID.TOP_10_TO_TOP_1, "top 10% to top 1%"),
            IncomeID.TOP_1_TO_TOP_0_1: Income(IncomeID.TOP_1_TO_TOP_0_1, "top 1% to top 0.1%"),
            IncomeID.TOP_0_1_TO_TOP_0_01: Income(IncomeID.TOP_0_1_TO_TOP_0_01, "top 0.1% to top 0.01%"),
            IncomeID.TOP_0_01_TO_TOP_0_001: Income(IncomeID.TOP_0_01_TO_TOP_0_001, "top 0.01% to top 0.001%"),
            IncomeID.TOP_0_001: Income(IncomeID.TOP_0_001, "top 0.001%")
        }
    """
    def __init__(self):
        """
        Initialize the IncomeMap object.
        """
        items: Dict[IncomeID, Income] = {
            IncomeID.UNKNOWN: Income(IncomeID.UNKNOWN, "unknown"),
            IncomeID.ZERO_TO_Q1: Income(IncomeID.ZERO_TO_Q1, "zero to q1"),
            IncomeID.Q1_TO_MEDIAN: Income(IncomeID.Q1_TO_MEDIAN, "q1 to median"),
            IncomeID.MEDIAN_TO_Q3: Income(IncomeID.MEDIAN_TO_Q3, "median to q3"),
            IncomeID.Q3_TO_TOP_10: Income(IncomeID.Q3_TO_TOP_10, "q3 to top 10%"),
            IncomeID.TOP_10_TO_TOP_1: Income(IncomeID.TOP_10_TO_TOP_1, "top 10% to top 1%"),
            IncomeID.TOP_1_TO_TOP_0_1: Income(IncomeID.TOP_1_TO_TOP_0_1, "top 1% to top 0.1%"),
            IncomeID.TOP_0_1_TO_TOP_0_01: Income(IncomeID.TOP_0_1_TO_TOP_0_01, "top 0.1% to top 0.01%"),
            IncomeID.TOP_0_01_TO_TOP_0_001: Income(IncomeID.TOP_0_01_TO_TOP_0_001, "top 0.01% to top 0.001%"),
            IncomeID.TOP_0_001: Income(IncomeID.TOP_0_001, "top 0.001%")
        }
        super().__init__(items)
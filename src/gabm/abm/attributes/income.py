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
<<<<<<< HEAD
from gabm.core.abm.attribute import GABMAttribute, GABMAttributeMap
=======
from gabm.abm.attribute import GABMAttribute, GABMAttributeMap
>>>>>>> upstream/main

class IncomeID(GABMID):
    """
    A unique identifier for an Income instance.
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
    By default, the map is initialized as follows:
        i0 = IncomeID(0)
        i1 = IncomeID(1)
        i2 = IncomeID(2)
        i3 = IncomeID(3)
        i4 = IncomeID(4)
        i5 = IncomeID(5)
        i6 = IncomeID(6)
        i7 = IncomeID(7)
        i8 = IncomeID(8)
        i9 = IncomeID(9)
        items: Dict[IncomeID, Income] = {
            i0: Income(i0, "unknown"),
            i1: Income(i1, "zero to q1"),
            i2: Income(i2, "q1 to median"),
            i3: Income(i3, "median to q3"),
            i4: Income(i4, "q3 to top 10%"),
            i5: Income(i5, "top 10% to top 1%"),
            i6: Income(i6, "top 1% to top 0.1%"),
            i7: Income(i7, "top 0.1% to top 0.01%"),
            i8: Income(i8, "top 0.01% to top 0.001%"),
            i9: Income(i9, "top 0.001%")
        }
    """
    def __init__(self):
        """
        Initialize the IncomeMap object.
        """
        i0 = IncomeID(0)
        i1 = IncomeID(1)
        i2 = IncomeID(2)
        i3 = IncomeID(3)
        i4 = IncomeID(4)
        i5 = IncomeID(5)
        i6 = IncomeID(6)
        i7 = IncomeID(7)
        i8 = IncomeID(8)
        i9 = IncomeID(9)
        items: Dict[IncomeID, Income] = {
            i0: Income(i0, "unknown"),
            i1: Income(i1, "zero to q1"),
            i2: Income(i2, "q1 to median"),
            i3: Income(i3, "median to q3"),
            i4: Income(i4, "q3 to top 10%"),
            i5: Income(i5, "top 10% to top 1%"),
            i6: Income(i6, "top 1% to top 0.1%"),
            i7: Income(i7, "top 0.1% to top 0.01%"),
            i8: Income(i8, "top 0.01% to top 0.001%"),
            i9: Income(i9, "top 0.001%")
        }
        super().__init__(items)
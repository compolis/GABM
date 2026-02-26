"""
Employment module for GABM.
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

class EmploymentID(GABMID):
    """
    A unique identifier for an Employment instance.
    Attributes:
        id (int): The unique identifier for the employment.
    """
    def __init__(self, employment_id: int):
        """
        Initialize
        Args:
            employment_id (int): The unique identifier for the employment.
        """
        super().__init__(employment_id)

class Employment(GABMAttribute):
    """
    For representing employment.
    Attributes:
        id (EmploymentID): Unique identifier for the employment.
        description (str): The description of the employment.
    """
    def __init__(self, employment_id: EmploymentID, description: str):
        super().__init__(employment_id, description)

class EmploymentMap(GABMAttributeMap):
    """
    A mapping of EmploymentIds to Employment.
    By default, the map is initialized as follows:
        e0 = EmploymentID(0)
        e1 = EmploymentID(1)
        e2 = EmploymentID(2)
        e3 = EmploymentID(3)
        e4 = EmploymentID(4)
        e5 = EmploymentID(5)
        e6 = EmploymentID(6)
        items: Dict[EmploymentID, Employment] = {
            e0: Employment(e0, "unknown"),
            e1: Employment(e1, "employed full time"),
            e2: Employment(e2, "employed part time"),
            e3: Employment(e3, "unemployed"),
            e4: Employment(e4, "student"),
            e5: Employment(e5, "retired")
            e6: Employment(e6, "economically inactive")
        }
        super().__init__(items)
    """
    def __init__(self):
        e0 = EmploymentID(0)
        e1 = EmploymentID(1)
        e2 = EmploymentID(2)
        e3 = EmploymentID(3)
        e4 = EmploymentID(4)
        e5 = EmploymentID(5)
        e6 = EmploymentID(6)
        items = {
            e0: Employment(e0, "unknown"),
            e1: Employment(e1, "employed full time"),
            e2: Employment(e2, "employed part time"),
            e3: Employment(e3, "unemployed"),
            e4: Employment(e4, "student"),
            e5: Employment(e5, "retired"),
            e6: Employment(e6, "economically inactive")
        }
        super().__init__(items)
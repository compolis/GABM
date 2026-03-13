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
from gabm.abm.attribute import GABMAttributeID, GABMAttribute, GABMAttributeMap

class EmploymentID(GABMAttributeID):
    """
    A unique identifier for an Employment attribute.

    Attributes:
        id (int): The unique identifier for the employment class instance.
    """
    def __init__(self, employment_id: int):
        """
        Initialize
        Args:
            employment_id (int): The unique identifier for the employment class instance.
        """
        super().__init__(employment_id)

# Standard EmploymentID constants for clarity and maintainability
EmploymentID.UNKNOWN = EmploymentID(0)
EmploymentID.EMPLOYED_FULL_TIME = EmploymentID(1)
EmploymentID.EMPLOYED_PART_TIME = EmploymentID(2)
EmploymentID.UNEMPLOYED = EmploymentID(3)
EmploymentID.STUDENT = EmploymentID(4)
EmploymentID.RETIRED = EmploymentID(5)
EmploymentID.ECONOMICALLY_INACTIVE = EmploymentID(6)

class Employment(GABMAttribute):
    """
    Employment class.

    Attributes:
        id (EmploymentID): Unique identifier for the employment.
        description (str): The description of the employment.
    """
    def __init__(self, employment_id: EmploymentID, description: str):
        """
        Initialize
        Args:
            employment_id (EmploymentID): The unique identifier for the employment.
            description (str): The description of the employment.
        """
        super().__init__(employment_id, description)

class EmploymentMap(GABMAttributeMap):
    """
    A mapping of EmploymentIds to Employment.

    By default, the map is initialized as follows::

        items = {
            EmploymentID.UNKNOWN: Employment(EmploymentID.UNKNOWN, "unknown"),
            EmploymentID.EMPLOYED_FULL_TIME: Employment(EmploymentID.EMPLOYED_FULL_TIME, "employed full time"),
            EmploymentID.EMPLOYED_PART_TIME: Employment(EmploymentID.EMPLOYED_PART_TIME, "employed part time"),
            EmploymentID.UNEMPLOYED: Employment(EmploymentID.UNEMPLOYED, "unemployed"),
            EmploymentID.STUDENT: Employment(EmploymentID.STUDENT, "student"),
            EmploymentID.RETIRED: Employment(EmploymentID.RETIRED, "retired"),
            EmploymentID.ECONOMICALLY_INACTIVE: Employment(EmploymentID.ECONOMICALLY_INACTIVE, "economically inactive")
        }
        super().__init__(items)

    """
    def __init__(self):
        items = {
            EmploymentID.UNKNOWN: Employment(EmploymentID.UNKNOWN, "unknown"),
            EmploymentID.EMPLOYED_FULL_TIME: Employment(EmploymentID.EMPLOYED_FULL_TIME, "employed full time"),
            EmploymentID.EMPLOYED_PART_TIME: Employment(EmploymentID.EMPLOYED_PART_TIME, "employed part time"),
            EmploymentID.UNEMPLOYED: Employment(EmploymentID.UNEMPLOYED, "unemployed"),
            EmploymentID.STUDENT: Employment(EmploymentID.STUDENT, "student"),
            EmploymentID.RETIRED: Employment(EmploymentID.RETIRED, "retired"),
            EmploymentID.ECONOMICALLY_INACTIVE: Employment(EmploymentID.ECONOMICALLY_INACTIVE, "economically inactive")
        }
        super().__init__(items)
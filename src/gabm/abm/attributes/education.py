"""
Education module for GABM.
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

class EducationID(GABMAttributeID):
    """
    Identifier for Education attributes.

    Attributes:
        id (int): The unique identifier.
    """
    def __init__(self, education_id: int):
        """
        Initialize.

        Args:
            education_id (int):
                The unique identifier for the education.

        """
        super().__init__(education_id)

# Standard EducationID constants for clarity and maintainability
EducationID.UNKNOWN = EducationID(0)
EducationID.PRIMARY = EducationID(1)
EducationID.SECONDARY = EducationID(2)
EducationID.COLLEGE = EducationID(3)
EducationID.UNIVERSITY = EducationID(4)
EducationID.DOCTORATE = EducationID(5)

class Education(GABMAttribute):
    """
    For representing education attributes.

    Attributes:
        id (EducationID): Unique identifier for the education attribute.
        description (str): The description of the education attribute.
    """
    def __init__(self, education_id: EducationID, description: str):
        """
        Initialize
        Args:
            education_id (EducationID): The unique identifier for the education attribute.
            description (str): The description of the education attribute.
        """
        super().__init__(education_id, description)

class EducationMap(GABMAttributeMap):
    """
    A mapping of EducationIds to Education.

    By default, the map is initialized as follows::

        items: Dict[EducationID, Education] = {
            EducationID.UNKNOWN: Education(EducationID.UNKNOWN, "unknown"),
            EducationID.PRIMARY: Education(EducationID.PRIMARY, "primary"),
            EducationID.SECONDARY: Education(EducationID.SECONDARY, "secondary"),
            EducationID.COLLEGE: Education(EducationID.COLLEGE, "college"),
            EducationID.UNIVERSITY: Education(EducationID.UNIVERSITY, "university"),
            EducationID.DOCTORATE: Education(EducationID.DOCTORATE, "doctorate")
        }
        super().__init__(items)
    """
    def __init__(self):
        items: Dict[EducationID, Education] = {
            EducationID.UNKNOWN: Education(EducationID.UNKNOWN, "unknown"),
            EducationID.PRIMARY: Education(EducationID.PRIMARY, "primary"),
            EducationID.SECONDARY: Education(EducationID.SECONDARY, "secondary"),
            EducationID.COLLEGE: Education(EducationID.COLLEGE, "college"),
            EducationID.UNIVERSITY: Education(EducationID.UNIVERSITY, "university"),
            EducationID.DOCTORATE: Education(EducationID.DOCTORATE, "doctorate")
        }
        super().__init__(items)
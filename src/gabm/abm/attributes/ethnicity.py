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

class EthnicityID(GABMAttributeID):
    """
    A unique identifier for an Ethnicity attribute.

    Attributes:
        id (int): The unique identifier for the ethnicity.
    """
    def __init__(self, ethnicity_id: int):
        """
        Initialize
        Args:
            ethnicity_id (int): The unique identifier for the ethnicity.
        """
        super().__init__(ethnicity_id)

# Standard EthnicityID constants for clarity and maintainability
EthnicityID.UNKNOWN = EthnicityID(0)
EthnicityID.AFRICAN = EthnicityID(1)
EthnicityID.AMERICAN = EthnicityID(2)
EthnicityID.ANTIPODIAN = EthnicityID(3)
EthnicityID.ASIAN = EthnicityID(4)
EthnicityID.EUROPEAN = EthnicityID(5)
EthnicityID.OTHER = EthnicityID(6)

class Ethnicity(GABMAttribute):
    """
    An Ethnicity.

    Attributes:
        id (EthnicityID): Unique identifier for the ethnicity.
        description (str): The description of the ethnicity.
    """
    def __init__(self, ethnicity_id: EthnicityID, description: str):
        """
        Initialize
        Args:
            ethnicity_id (EthnicityID): The unique identifier for the ethnicity.
            description (str): The description of the ethnicity.
        """
        super().__init__(ethnicity_id, description)

class EthnicityMap(GABMAttributeMap):
    """
    A mapping of EthnicityIds to Ethnicity.

    By default, the map is initialized as follows::

        items: Dict[EthnicityID, Ethnicity] = {
            EthnicityID.UNKNOWN: Ethnicity(EthnicityID.UNKNOWN, "unknown"),
            EthnicityID.AFRICAN: Ethnicity(EthnicityID.AFRICAN, "african"),
            EthnicityID.AMERICAN: Ethnicity(EthnicityID.AMERICAN, "american"),
            EthnicityID.ANTIPODIAN: Ethnicity(EthnicityID.ANTIPODIAN, "antipodian"),
            EthnicityID.ASIAN: Ethnicity(EthnicityID.ASIAN, "asian"),
            EthnicityID.EUROPEAN: Ethnicity(EthnicityID.EUROPEAN, "european"),
            EthnicityID.OTHER: Ethnicity(EthnicityID.OTHER, "other")
        }
        super().__init__(items)
    """
    def __init__(self):
        """
        Initialize the Ethnicities object.
        """
        items: Dict[EthnicityID, Ethnicity] = {
            EthnicityID.UNKNOWN: Ethnicity(EthnicityID.UNKNOWN, "unknown"),
            EthnicityID.AFRICAN: Ethnicity(EthnicityID.AFRICAN, "african"),
            EthnicityID.AMERICAN: Ethnicity(EthnicityID.AMERICAN, "american"),
            EthnicityID.ANTIPODIAN: Ethnicity(EthnicityID.ANTIPODIAN, "antipodian"),
            EthnicityID.ASIAN: Ethnicity(EthnicityID.ASIAN, "asian"),
            EthnicityID.EUROPEAN: Ethnicity(EthnicityID.EUROPEAN, "european"),
            EthnicityID.OTHER: Ethnicity(EthnicityID.OTHER, "other")
        }
        super().__init__(items)
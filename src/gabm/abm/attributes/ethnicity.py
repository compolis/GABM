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
<<<<<<< HEAD
from gabm.core.abm.attribute import GABMAttribute, GABMAttributeMap
=======
from gabm.abm.attribute import GABMAttribute, GABMAttributeMap
>>>>>>> upstream/main

class EthnicityID(GABMID):
    """
    A unique identifier for an Ethnicity instance.
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
        super().__init__(employment_id, description)

class EthnicityMap(GABMAttributeMap):
    """
    A mapping of EthnicityIds to Ethnicity.
    By default, the map is initialized as follows:
        e0 = EthnicityID(0)
        e1 = EthnicityID(1)
        e2 = EthnicityID(2)
        e3 = EthnicityID(3)
        e4 = EthnicityID(4)
        e5 = EthnicityID(5)
        items: Dict[EthnicityID, Ethnicity] = {
            e0: Ethnicity(e0, "unknown"),
            e1: Ethnicity(e1, "white"),
            e2: Ethnicity(e2, "asian"),
            e3: Ethnicity(e3, "black"),
            e4: Ethnicity(e4, "mixed"),
            e5: Ethnicity(e5, "other")
        }
        super().__init__(items)
    """
    def __init__(self):
        """
        Initialize the Ethnicities object.
        """
        e0 = EthnicityID(0)
        e1 = EthnicityID(1)
        e2 = EthnicityID(2)
        e3 = EthnicityID(3)
        e4 = EthnicityID(4)
        e5 = EthnicityID(5)
        items: Dict[EthnicityID, Ethnicity] = {
            e0: Ethnicity(e0, "unknown"),
            e1: Ethnicity(e1, "white"),
            e2: Ethnicity(e2, "asian"),
            e3: Ethnicity(e3, "black"),
            e4: Ethnicity(e4, "mixed"),
            e5: Ethnicity(e5, "other")
        }
        super().__init__(items)
"""
Health module for GABM.
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

class HealthID(GABMAttributeID):
    """
    A unique identifier for a Health attribute.

    Attributes:
        id (int): The unique identifier for the health attribute.
    """
    def __init__(self, health_id: int):
        """
        Initialize
        Args:
            health_id (int): The unique identifier for the health attribute.
        """
        super().__init__(health_id)

# Standard HealthID constants for clarity and maintainability
HealthID.UNKNOWN = HealthID(0)
HealthID.VERY_GOOD = HealthID(1)
HealthID.GOOD = HealthID(2)
HealthID.FAIR = HealthID(3)
HealthID.BAD = HealthID(4)
HealthID.VERY_BAD = HealthID(5)

class Health(GABMAttribute):
    """
    For representing health.

    Attributes:
        id (HealthID): Unique identifier for the health.
        description (str): The description of the health.
    """
    def __init__(self, health_id: HealthID, description: str):
        """
        Initialize
        Args:
            health_id (HealthID): The unique identifier for the self reported health status.
            description (str): The description of the self reported health status.
        """
        super().__init__(health_id, description)

class HealthMap(GABMAttributeMap):
    """
    A mapping of HealthIds to Health.

    By default, the map is initialized as follows::

        h0 = HealthID(0)
        h1 = HealthID(1)
        h2 = HealthID(2)
        h3 = HealthID(3)
        h4 = HealthID(4)
        h5 = HealthID(5)
        items: Dict[HealthID, Health] = {
            h0: Health(h0, "unknown"),
            h1: Health(h1, "very good"),
            h2: Health(h2, "good"),
            h3: Health(h3, "fair"),
            h4: Health(h4, "bad"),
            h5: Health(h5, "very bad")
        }
        super().__init__(items)
    """
    def __init__(self):
        h0 = HealthID(0)
        h1 = HealthID(1)
        h2 = HealthID(2)
        h3 = HealthID(3)
        h4 = HealthID(4)
        h5 = HealthID(5)
        items: Dict[HealthID, Health] = {
            h0: Health(h0, "unknown"),
            h1: Health(h1, "very good"),
            h2: Health(h2, "good"),
            h3: Health(h3, "fair"),
            h4: Health(h4, "bad"),
            h5: Health(h5, "very bad")
        }
        super().__init__(items)
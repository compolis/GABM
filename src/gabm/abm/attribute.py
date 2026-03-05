"""
Generic attribute base classes for GABM.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.2.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import logging
from typing import Dict, TypeVar, Generic
# Local imports
from gabm.core.id import GABMID

class GABMAttribute:
    """
    Generic base class for attributes (e.g., Gender, Health).

    Attributes:
        id: Unique identifier object (e.g., GenderID, HealthID).
        description (str): Description of the attribute.
    """
    def __init__(self, id: GABMID, description: str):
        self.id = id
        self.description = description

    def __str__(self):
        """
        Return:
            A string representation.
        """
        return f"{self.__class__.__name__}(id={self.id}, description='{self.description}')"

    def __repr__(self):
        """
        Return:
            Official string representation.
        """
        return self.__str__()

class GABMAttributeMap:
    """
    Generic base class for attribute maps (e.g., GenderMap, HealthMap).

    Attributes:
        _map (dict): Mapping from ID objects to attribute instances.
    """
    def __init__(self, items: dict[GABMID, GABMAttribute]):
        """
        Initialize.
        
        Args:
            items (dict[GABMID, GABMAttribute]): A dictionary mapping GABMID objects to GABMAttribute instances.
        """
        self._map: Dict[GABMID, T] = items

    T = TypeVar('T', bound=GABMAttribute)

    def get(self, id: GABMID):
        """
        Return:
            The attribute instance for the given ID object, or None if not found.
        """
        if not isinstance(id, GABMID):
            raise TypeError(f"Key must be a GABMID, got {type(id)}")
        return self._map.get(id)

    def add(self, attr: GABMAttribute):
        """
        Add an attribute to the map.

        Args:
            attr: An instance of an attribute (e.g., Gender, Health).
        """
        if not isinstance(attr, GABMAttribute):
            raise TypeError(f"Value must be an GABMAttribute, got {type(attr)}")
        if not isinstance(attr.id, GABMID):
            raise TypeError(f"Attribute id must be a GABMID, got {type(attr.id)}")
        self._map[attr.id] = attr

    def __getitem__(self, id_obj):
        """
        Return:
            The attribute instance for the given ID object.
        Raises:
            KeyError: If the ID object is not found in the map.
        """
        if not isinstance(id_obj, GABMID):
            raise TypeError(f"Key must be a GABMID, got {type(id_obj)}")
        return self._map[id_obj]

    def __iter__(self):
        """
        Return:
            An iterator over the attribute instances in the map.
        """
        return iter(self._map.values())

    def __len__(self):
        """
        Return:
            The number of attributes in the map.
        """
        return len(self._map)

    def __str__(self):
        """
        Return:
            A string representation.
        """
        return f"{self.__class__.__name__}({self._map})"

    def __repr__(self):
        """
        Return:
            A string representation.
        """
        return self.__str__()

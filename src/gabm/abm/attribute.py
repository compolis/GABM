"""
Attribute module for GABM.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.2.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


class GenderID:
    """
    A unique identifier for an Gender instance.
    Attributes:
        gender_id (int): The unique identifier for the gender.
    """
    def __init__(self, gender_id: int):
        self.id = gender_id

    def __str__(self):
        """
        Return:
            A string representation.
        """
        return f"GenderID({self.id})"

    def __repr__(self):
        """
        Return:
            A string representation.
        """
        return self.__str__()

class Gender:
    """
    A Gender.
    Attributes:
        id (GenderID): Unique identifier for the gender.
        value (int): The value of the gender.
        description (str): The description of the gender.
    """
    def __init__(self, gender_id: GenderID, value: int, description: str):
        """
        Initialize
        Args:
            gender_id (GenderID): The unique identifier for the gender.
            value (int): The value of the gender.
            description (str): The description of the gender.
        """
        self.id = gender_id
        self.value = value
        self.description = description

    def __str__(self):
        """
        Return:
            A string representation.
        """
        return self.description

    def __repr__(self):
        """
        Return:
            A string representation.
        """
        return self.__str__()

class Genders:
    """
    A mapping of GenderIds to Genders.
    The mapping can be extended to include more genders as needed.
    Attributes:
        gender_map (dict): A dictionary mapping GenderIds to Genders.
            The keys are GenderIds, and the values are Gender objects.
            The default mapping includes:
                0: "female",
                1: "male",
                2: "non-binary".
    """
    def __init__(self):
        """
        Initialize the Genders object.
        """
        g0 = GenderID(0)
        g1 = GenderID(1)
        g2 = GenderID(2)
        self.gender_map = {
            g0: Gender(g0, 0, "female"),
            g1: Gender(g1, 1, "male"),
            g2: Gender(g2, 2, "non-binary"),
        }

    def __str__(self):
        """
        Return:
            The string representation.
        """
        return self.gender_map[self.id]

    def __repr__(self):
        """
        Return:
            Official string representation.
        """
        return self.__str__()
    
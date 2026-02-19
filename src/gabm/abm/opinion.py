"""
Opinion module for GABM.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


class Opinion:
    """
    An Opinion is a value that can be associated with a Person, 
    OpinionatedGroup, and/or a OpinionatedEnvironment.
    Attributes:
        name (str): The name of the opinion.
        description (str): A description of the opinion.
        value (int): The value of the opinion.
    """
    def __init__(self, name: str, description: str, value: int):
        """
        Initialize
        """
        self.name = name
        self.description = description
        self.value = value
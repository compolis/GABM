

# CandidateID now extends BaseID
class CandidateID(BaseID):
    """
    A unique identifier for a Candidate instance.
    Attributes:
        candidate_id (int): The unique identifier for the candidate.
    """
    def __init__(self, candidate_id: int):
        super().__init__(candidate_id)

class Candidate():
    """
    For representing a candidate.
    Attributes:
        id (CandidateID): Unique identifier for the candidate.
        description (str): The description of the candidate.
    """
    def __init__(self, candidate_id: CandidateID, description: str):
        """
        Initialize
        Args:
            candidate_id (CandidateID): The unique identifier for the candidate.
            description (str): The description of the candidate.
        """
        self.id = candidate_id
        self.description = description
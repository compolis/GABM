"""
Survey module for GABM.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import logging
from typing import List, Dict, Any
# Local imports
from gabm.abm.agent import Person
from gabm.core.id import GABMID
from gabm.io.llm.llm_service import LLMService

class AnswerID(GABMID):
    """
    A unique identifier for a Answer instance.

    Attributes:
        id (int): The unique identifier for the answer.
    """
    def __init__(self, answer_id: int):
        """
        Initialize
        Args:
            answer_id: The unique identifier for the answer.
        """
        super().__init__(answer_id)

class Answer():
    """
    Represents a single answer to a question.

    Attributes:
        id (AnswerID): The id of the Answer
        text (str): The answer text.
        answers (List[Answer]): List of available Answers.
    """
    def __init__(self, answer_id: AnswerID, text: str):
        """
        Initialize
        Args:
            answer_id The unique identifier for the answer.
            text The text of the answer.
        """
        self.id = answer_id
        self.text = text

class QuestionID(GABMID):
    """
    A unique identifier for a Question instance.

    Attributes:
        id (int): The unique identifier for the question.
    """
    def __init__(self, question_id: int):
        """
        Initialize
        Args:
            question_id: The unique identifier for the question.
        """
        super().__init__(question_id)

class Question():
    """
    Represents a single survey question.

    Attributes:
        id (QuestionID): The question identifier.
        text (str): The question text.
        answers (List[Answer]): List of available Answers.
    """
    def __init__(self, question_id: QuestionID, text: str, answers: List["Answer"] = None):
        self.id = question_id
        self.text = text
        self.answers = answers or []

    def __str__(self):
        return f"Question(text={self.text})"

    def __repr__(self):
        return self.__str__()

    def get_prompt(self) -> str:
        """
        Get the LLM prompt for the question - the text and available answers.
        Returns:
            A string representation of the question context.
        """
        question_text = "I am asked: " + self.text
        question_text += ". I can choose from the following options: "
        answer_texts = [answer.text for answer in self.answers]
        return f"{question_text}{', '.join(answer_texts)}. What do I choose?"

    def add_answer(self, answer: Answer):
        """
        Add an answer to the question.
        Args:
            answer: The Answer instance to add.
        """
        self.answers.append(answer)

class Survey:
    """
    Represents a survey comprising multiple questions.

    Attributes:
        questions (List[Question]): The list of questions in the survey.
        title (str): The title of the survey.
        description (str): Description of the survey.
    """
    def __init__(self, questions: List[Question], title: str = "", description: str = ""):
        self.questions = questions
        self.title = title
        self.description = description

    def __str__(self):
        return f"Survey(title={self.title}, questions={len(self.questions)})"

    def __repr__(self):
        return self.__str__()

    def get_question(self, index: int) -> Question:
        return self.questions[index]

    def add_question(self, question: Question):
        self.questions.append(question)

# Placeholder for LLM interaction logic
class SurveyConversation:
    """
    Handles a conversation between a Person (with a Profile/Persona) and an LLM for survey response simulation.
    
    Attributes:
        person (Person): The person instance.
        survey (Survey): The survey to be conducted.
        llm_service (LLMService): The LLM service interface (to be implemented).
        api_key (str): The API key for the LLM service.
        model (str): The model to use for the LLM service.
        responses (List[str]): The list of responses from the LLM for each question.
    """
    def __init__(self, person: Person, survey: Survey, llm_service: LLMService,
            api_key: str = None, model: str = None):
        """
        Initialize
        Args:
            person: The Person instance.
            survey: The Survey instance.
            llm_service: The LLMService instance.
            api_key: The API key for the LLM service (optional, can be set via environment variable).
            model: The model to use for the LLM service (optional, can be determined by
        """
        self.person = person
        self.survey = survey
        self.llm_service = llm_service
        self.api_key = api_key or llm_service.get_api_key()
        self.model = model or llm_service.get_default_model()
        self.responses = []

    def conduct(self):
        """
        Conducts the survey by asking each question to the LLM with the given profile context.
        Stores responses in self.responses.
        """
        person_profile = self.person.profile
        for question in self.survey.questions:
            context = person_profile + " " + question.text  # In a real implementation, this would include more context about the person and the question
            response = self.llm_service.send(context, model=self.model, api_key=self.api_key)
            self.responses.append(response)

    def _build_context(self, question: Question) -> Dict[str, Any]:
        """
        Builds the context for the LLM, including the person's profile and the current question.
        """
        return {
            "profile": self.person_profile,
            "question": question.text,
            "options": question.options,
            "metadata": question.metadata
        }

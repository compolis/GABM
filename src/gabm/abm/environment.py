"""
Environment module for GABM.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.4.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import random
from typing import Callable, Dict
from pathlib import Path
from datetime import date, timedelta
# Local imports
from gabm.abm.agent import Agent
from gabm.abm.attributes.gender import GenderID
from gabm.abm.attributes.interest import InterestTopicID, InterestValue, InterestValueMap, Interest
from gabm.abm.attributes.opinion import OpinionTopicID, OpinionValue, OpinionValueMap, Opinion
from gabm.abm.group import Group
from gabm.abm.attributes.gender import GenderMap
from gabm.abm.attributes.region import RegionMap
from gabm.abm.attributes.education import EducationMap
from gabm.abm.attributes.employment import EmploymentMap
from gabm.abm.attributes.income import IncomeMap
from gabm.abm.attributes.trait import TraitTopicID, TraitValue, TraitValueMap, Trait

class Environment():
    """
    An Environment with opinions.

    Attributes:
        year (int):
            The current year in the simulation.
        name (str):
            The name of the environment.
        agents_active (Dict[AgentID, Agent]):
            A dictionary of active agents in the environment.
        agents_inactive (Dict[AgentID, Agent]):
            A dictionary of inactive agents in the environment.
        groups_active (Dict[GroupID, Group]):
            A dictionary of active groups in the environment.
        groups_inactive (Dict[GroupID, Group]):
            A dictionary of inactive groups in the environment.
        gender_map (GenderMap):
            A map for gender attribute lookups.
        interests (Dict[InterestTopicID, InterestValue]):
            A dictionary of interests.
            The key is an InterestTopicID, the value is an InterestValue object.
        opinions (Dict[OpinionTopicID, OpinionValue]):
            A dictionary of opinions.
            The key is an OpinionTopicID, the value is an OpinionValue object.
    """

    def __init__(self, year: int = 2026, name: str = "Earth",
        current_date: date = None,
        gender_map: GenderMap = None,
        interests: Dict[InterestTopicID, InterestValue] = None,
        opinions: Dict[OpinionTopicID, OpinionValue] = None):
        """
        Initialize.

        Args:
            year (int):
                The current year in the simulation.
            current_date (date):
                Optional simulation calendar date for sub-year stepping.
            name (str):
                The name of the environment.
            gender_map (GenderMap):
                A GenderMap instance for gender attribute lookups.
            interests (Dict[InterestTopicID, InterestValue]):
                A dictionary of interests, where the key is an InterestTopicID and the value is an InterestValue object.
                This allows the environment to have an overview of interests of Persons and InterestGroups.
            opinions (Dict[OpinionTopicID, OpinionValue]):
                A dictionary of opinions, where the key is an OpinionTopicID and the value is an OpinionValue object.
                This allows the environment to have an overview of opinions of Persons and OpinionatedGroups.
            
        """
        if current_date is None:
            self.current_date = date(year, 1, 1)
        else:
            self.current_date = current_date
        self.year = self.current_date.year
        self.name = "Earth" if name is None else name
        self.agents_active: Dict = {}
        self.agents_inactive: Dict = {}
        self.groups_active: Dict = {}
        self.groups_inactive: Dict = {}
        self.gender_map = gender_map if gender_map is not None else GenderMap()
        self.interests = interests if interests is not None else {}
        self.opinions = opinions if opinions is not None else {}

    def get_birthdays_on(self, on_date: date = None):
        """
        Return active agents whose birthday occurs on the specified date.

        Args:
            on_date: Date to check. Defaults to environment current_date.

        Returns:
            List of agents with a matching birthday.
        """
        target_date = self.current_date if on_date is None else on_date
        birthdays = []
        for agent in self.agents_active.values():
            is_birthday = getattr(agent, "is_birthday", None)
            if callable(is_birthday) and is_birthday(target_date.month, target_date.day):
                birthdays.append(agent)
        return birthdays

    def advance_day(self, days: int = 1, birthday_callback: Callable | None = None):
        """
        Advance simulation date by whole days and emit birthday events.

        Args:
            days: Number of days to advance.
            birthday_callback: Optional callback invoked as callback(person, date).

        Returns:
            List of (person, date) birthday events encountered during stepping.
        """
        if days < 0:
            raise ValueError("days must be >= 0")

        events = []
        for _ in range(days):
            self.current_date = self.current_date + timedelta(days=1)
            self.year = self.current_date.year
            for person in self.get_birthdays_on(self.current_date):
                events.append((person, self.current_date))
                if birthday_callback is not None:
                    birthday_callback(person, self.current_date)
        return events

    def __str__(self):
        """
        Return:
            A string representation.
        """
        class_name = self.__class__.__name__
        return f"{class_name}: year={self.year}, name='{self.name}', " \
               f"agents_active={len(self.agents_active)}, agents_inactive={len(self.agents_inactive)}, " \
               f"groups_active={len(self.groups_active)}, groups_inactive={len(self.groups_inactive)}, " \
               f"gender_map={self.gender_map}, " \
               f"interests={len(self.interests)}, " \
               f"opinions={len(self.opinions)}"

    def __repr__(self):
        """
        Return:
            An official string representation.
        """
        return self.__str__()

    def create_random_people(
        self,
        count: int,
        start_person_id: int = 1,
        seed: int = None,
        with_interests: bool = False,
        year_of_birth_min: int = 1970,
        year_of_birth_max: int = 2000,
        age_min: int = None,
        age_max: int = None,
        ons_male_file: Path = None,
        ons_female_file: Path = None,
    ):
        """
        Create and register random Person agents.

        Args:
            count: Number of people to create.
            start_person_id: First person ID; subsequent people increment by 1.
            seed: Optional deterministic seed for reproducibility.
            with_interests: If True, generate default trait-guided interests too.
            year_of_birth_min: Minimum year of birth to sample.
            year_of_birth_max: Maximum year of birth to sample.
            age_min: Optional minimum age in years to sample from.
            age_max: Optional maximum age in years to sample from.
            ons_male_file: Optional path to ONS male names CSV used for Person auto-naming.
            ons_female_file: Optional path to ONS female names CSV used for Person auto-naming.

        Returns:
            List of created Person instances.
        """
        if count < 0:
            raise ValueError("count must be >= 0")
        if (age_min is None) != (age_max is None):
            raise ValueError("age_min and age_max must be provided together")
        if age_min is not None:
            if age_min < 0 or age_max < 0:
                raise ValueError("age_min and age_max must be >= 0")
            if age_min > age_max:
                raise ValueError("age_min must be <= age_max")
        if year_of_birth_min > year_of_birth_max:
            raise ValueError("year_of_birth_min must be <= year_of_birth_max")

        # Local import avoids circular runtime dependency (agent imports Environment for typing).
        from gabm.abm.agent import Person, PersonID

        rng = random if seed is None else random.Random(seed)
        people = []
        for offset in range(count):
            person_id = PersonID(start_person_id + offset)
            sampled_age = None
            if age_min is not None:
                sampled_age = rng.randint(age_min, age_max)
                year_of_birth = None
            else:
                year_of_birth = rng.randint(year_of_birth_min, year_of_birth_max)
            gender_id = GenderID(rng.randint(1, 2))

            # Use independent deterministic seeds so trait generation and
            # interest generation are reproducible without being tightly coupled.
            trait_seed = rng.randint(0, 2**31 - 1)
            interest_seed = rng.randint(0, 2**31 - 1) if with_interests else None

            person = Person.with_random_traits(
                person_id=person_id,
                environment=self,
                year_of_birth=year_of_birth,
                gender_id=gender_id,
                age=sampled_age,
                ons_male_file=ons_male_file,
                ons_female_file=ons_female_file,
                seed=trait_seed,
                generate_interests=with_interests,
                interest_seed=interest_seed,
            )
            self.agents_active[person.id] = person
            people.append(person)

        return people

class Nation(Environment):
    """
    An Environment representing a nation.
    Can be extended with nation-specific attributes and methods.
    
    .. note::
            Inherits all attributes from :class:`Environment`.

    Attributes:
        citizens (Group):
            A group of Person agents representing the citizens of the nation.
        visitors (Group):
            A group of Person agents representing the visitors in the nation.
        region_map (UKRegionMap):
            A UKRegionMap instance for region attribute lookups.
        education_map (SurveyEducationMap):
            A SurveyEducationMap instance for education attribute lookups.
        employment_map (SurveyEmploymentMap):
            A SurveyEmploymentMap instance for employment attribute lookups.
        income_map (SurveyIncomeMap):
            A SurveyIncomeMap instance for income attribute lookups.
        name (str):
            The name of the nation.
    """
    
    def __init__(self, year: int = 2026, name: str = "Earth", 
        gender_map: GenderMap = None,
        interests: Dict[InterestTopicID, InterestValue] = None,
        opinions: Dict[OpinionTopicID, OpinionValue] = None,
        region_map: RegionMap = None,
        education_map: EducationMap = None,
        employment_map: EmploymentMap = None,
        income_map: IncomeMap = None):
        """
        Initialize.
        Args:
            year (int):
                The current year in the simulation.
            interests (Dict[InterestTopicID, InterestValue]):
                A dictionary of interests in the nation.
            gender_map (GenderMap):
                A GenderMap instance for gender attribute lookups.
            region_map (RegionMap):
                A RegionMap instance for region attribute lookups.
            education_map (EducationMap):
                An EducationMap instance for education attribute lookups.
            opinions (Dict[OpinionTopicID, Opinion]):
                A dictionary of opinions, where the key is an OpinionTopicID and the value is an Opinion object.
                This allows the environment to have an overview of opinions of Persons and OpinionatedGroups.
        """
        super().__init__(
            year=year,
            name=name,
            gender_map=gender_map,
            interests=interests,
            opinions=opinions,
        )
        self.region_map = region_map if region_map is not None else RegionMap()
        self.education_map = education_map if education_map is not None else EducationMap()
        self.employment_map = employment_map if employment_map is not None else EmploymentMap()
        self.income_map = income_map if income_map is not None else IncomeMap()
        from gabm.abm.group import Group, GroupID
        self.citizens = Group(GroupID(1), name="Citizens")
        self.groups_active[self.citizens.id] = self.citizens
        self.visitors = Group(GroupID(2), name="Visitors")
        self.groups_active[self.visitors.id] = self.visitors
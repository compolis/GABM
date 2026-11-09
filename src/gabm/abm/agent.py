# NOTE: This import must be the very first non-empty line in the file (even before docstrings)
# due to Python syntax rules for __future__ imports.
from __future__ import annotations
"""
Agent module for GABM.

For representing an entity within an Environment. The Agent class is a base class for more specific agent types, such as Person and Citizen.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.2.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Standard library imports
from typing import TYPE_CHECKING, Set
from dataclasses import dataclass, field
import copy
import logging
import random
from types import MappingProxyType
from pathlib import Path
from datetime import date
# Local imports
from gabm.core.id import GABMID
from gabm.abm.attributes.gender import GenderID
from gabm.abm.attributes.interest import InterestTopicID, InterestTopic, Interest, InterestValue, InterestValueMap
from gabm.abm.attributes.opinion import OpinionTopicID, OpinionValue, OpinionValueMap, Opinion
from gabm.abm.attributes.region import RegionID, RegionMap
from gabm.abm.attributes.education import EducationID, Education, EducationMap
from gabm.abm.attributes.employment import EmploymentID, EmploymentMap
from gabm.abm.attributes.health import HealthID, HealthMap
from gabm.abm.attributes.income import IncomeID, IncomeMap
from gabm.abm.attributes.trait import TraitTopicID, TraitValue, TraitValueMap, Trait
from gabm.abm.attributes.values import ValueTopicID, Values
from gabm.abm.attributes.wealth import WealthID, Wealth
from gabm.abm.data.names_ons import choose_name_for_person, get_default_ons_name_paths, load_ons_name_table
# TYPE_CHECKING is used to avoid circular imports.
if TYPE_CHECKING:
    from gabm.abm.environment import Environment, Nation
    from gabm.abm.group import Group, OpinionGroup

class AgentID(GABMID):
    """
    A unique identifier for an Agent instance.

    Attributes:
        id (int): The unique identifier for the agent.
    """
    def __init__(self, id: int):
        """
        Initialize
        Args:
            id (int): The unique identifier for the agent.
        """
        super().__init__(id)

class Agent():
    """
    For representing an entity within an Environment.
    The type annotation for environment is quoted as it is imported
    under TYPE_CHECKING to avoid circular imports.

    Attributes:
        agent_id (AgentID):
            Unique identifier for the Agent instance.
        environment (Environment):
            The Environment the Agent instance belongs to.
        groups (Set[Group]):
            A Set of Groups that the Agent instance belongs to.
    """
    def __init__(self, agent_id: int | AgentID, environment: Environment):
        """
        Initialize.
        Args:
            agent_id: Unique identifier for the Agent instance.
            environment: The shared environment the Agent instance belongs to.
        """
        if isinstance(agent_id, int):
            self.id = AgentID(agent_id)
        elif not isinstance(agent_id, AgentID):
            raise TypeError("agent_id must be an int or an AgentID")
        self.id = agent_id if isinstance(agent_id, AgentID) else AgentID(agent_id)
        self.environment = environment
        self.groups: Set['Group'] = set()

    def __str__(self):
        """
        Return:
            String representation.
        """
        return f"Agent (id={self.id}, groups={len(self.groups)})" 
    
    def __repr__(self):
        """
        Return:
            Official String representation.
        """
        return self.__str__()

    def join_group(self, group: 'Group'):
        """
        Join group.
        
        This updates group membership.

        Args:
            group: The Group instance to join.
        """
        group.add_member(self)

    def leave_group(self, group: 'Group'):
        """
        Leave group.
        
        This updates group membership.

        Args:
            group: The Group instance to leave.
        """
        group.remove_member(self)


@dataclass
class TraitBeliefState:
    """
    Typed container for trait beliefs.

    ``self_trait_opinions`` stores a person's perceived values of their own
    base traits.

    ``other_trait_opinions`` stores nested values keyed as:
    ``other_agent_id -> order -> trait_topic_id -> value``.
    """
    self_trait_opinions: dict[TraitTopicID, float] = field(default_factory=dict)
    other_trait_opinions: dict[AgentID, dict[int, dict[TraitTopicID, float]]] = field(default_factory=dict)

    def set_self_opinion(self, trait_id: TraitTopicID, value: float):
        self.self_trait_opinions[trait_id] = value

    def get_self_opinion(self, trait_id: TraitTopicID) -> float:
        return self.self_trait_opinions.get(trait_id)

    @staticmethod
    def _normalize_agent_id(other_agent_id: int | AgentID) -> AgentID:
        if isinstance(other_agent_id, AgentID):
            return other_agent_id
        return AgentID(other_agent_id)

    def set_other_opinion(self,
        other_agent_id: int | AgentID,
        trait_id: TraitTopicID,
        value: float,
        order: int = 1):
        if order < 1:
            raise ValueError("order must be >= 1")
        normalized_id = self._normalize_agent_id(other_agent_id)
        self.other_trait_opinions.setdefault(normalized_id, {})
        self.other_trait_opinions[normalized_id].setdefault(order, {})
        self.other_trait_opinions[normalized_id][order][trait_id] = value

    def get_other_opinion(self,
        other_agent_id: int | AgentID,
        trait_id: TraitTopicID,
        order: int = 1) -> float:
        if order < 1:
            raise ValueError("order must be >= 1")
        normalized_id = self._normalize_agent_id(other_agent_id)
        if normalized_id not in self.other_trait_opinions:
            return None
        return self.other_trait_opinions[normalized_id].get(order, {}).get(trait_id)

    def to_dict(self) -> dict:
        return {
            "self_trait_opinions": {
                trait_id.id: value for trait_id, value in self.self_trait_opinions.items()
            },
            "other_trait_opinions": {
                other_id.id: {
                    order: {trait_id.id: value for trait_id, value in trait_map.items()}
                    for order, trait_map in order_map.items()
                }
                for other_id, order_map in self.other_trait_opinions.items()
            },
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TraitBeliefState":
        state = cls()
        for trait_id, value in data.get("self_trait_opinions", {}).items():
            state.self_trait_opinions[TraitTopicID(int(trait_id))] = value

        for other_id, order_map in data.get("other_trait_opinions", {}).items():
            normalized_other = AgentID(int(other_id))
            state.other_trait_opinions[normalized_other] = {}
            for order, trait_map in order_map.items():
                normalized_order = int(order)
                state.other_trait_opinions[normalized_other][normalized_order] = {}
                for trait_id, value in trait_map.items():
                    state.other_trait_opinions[normalized_other][normalized_order][TraitTopicID(int(trait_id))] = value
        return state

class PersonID(AgentID):
    """
    Person ID
    """
    def __init__(self, id: int):
        """
        Initialize.

        Args:
            id: Unique identifier for the Person instance.
        """
        super().__init__(id)

class Person(Agent):
    """
    An Agent with a year of birth and Gender.

    .. note::
            Inherits all attributes from :class:`Agent`.

    Attributes:
        year_of_birth (int):
            The year of birth attributed.
        gender_id (GenderID):
            The GenderID attributed.
        interests (Dict[InterestTopicID, Interest]):
            A dictionary of Interests.
            The keys are InterestTopicIDs, and the values are Interest objects.
            These are deep copied when the Person is initialised, so that the Person has their own
        opinions (Dict[OpinionTopicID, Opinion]):
            A dictionary of Opinions.
            The keys are OpinionTopicIDs, and the values are Opinion objects.
            These are deep copied when the Person is initialised, so that the Person has their own opinions.
    """
    _ons_table_cache = {}

    def __init__(self, person_id: PersonID, environment: Environment,
        year_of_birth: int, gender_id: GenderID,
        age: int = None,
        age_min: int = None,
        age_max: int = None,
        date_of_birth: date = None,
        name: str = None,
        traits: dict[TraitTopicID, 'Trait'] = None,
        interests: dict[InterestTopicID, 'Interest'] = None,
        opinions: dict[OpinionTopicID, 'Opinion'] = None,
        values: dict[ValueTopicID, 'Values'] = None,
        ons_male_file: Path = None,
        ons_female_file: Path = None,
        value_economic_security: str = "medium",
        value_stochastic: bool = False,
        value_seed: int = None):
        """
        Initialize

        Args:
            person_id: Unique identifier for the Person instance.
            environment: The Environment the Person instance belongs to.
            year_of_birth: The year the person was born.
            age: Optional exact age in years.
            age_min: Optional minimum age in years.
            age_max: Optional maximum age in years.
            date_of_birth: Optional full birth date.
            gender_id: The GenderID attributed.
            name: Optional display name for the person. If not provided, auto-assigned from ONS tables.
            traits: A dictionary of traits, where keys are TraitTopicIDs and values are Trait objects.interests: A dictionary of interests, where keys are InterestTopicIDs and values are Interest objects.
            opinions: A dictionary of opinions, where keys are OpinionTopicIDs and values are Opinion objects.
            values: A dictionary of value-priority attributes where keys are ValueTopicIDs and values are Values objects.
            ons_male_file: Optional path to ONS male names CSV for auto-assignment.
            ons_female_file: Optional path to ONS female names CSV for auto-assignment.
            value_economic_security: Economic-security context used when auto-generating values.
            value_stochastic: If True, include stochastic jitter when auto-generating values.
            value_seed: Optional deterministic seed used when auto-generating values.
            
        """
        super().__init__(agent_id=person_id, environment=environment)
        self.gender_id = gender_id
        # Robust gender_map checking for mocks and real objects
        gender_map = getattr(environment, 'gender_map', None)
        if self.gender_id is not None and gender_map is None:
            message = f"Gender value {self.gender_id} is provided but no gender map is provided. Cannot interpret gender value."
            logging.warning(message)
            raise ValueError(message)
        # Only check for key if gender_map is a real dict-like object
        if self.gender_id is not None and gender_map is not None:
            try:
                # Try to check if gender_id is in gender_map (works for dict, GenderMap, but not for Mock)
                if hasattr(gender_map, '__contains__') and not self.gender_id in gender_map:
                    debug_info = (
                        f"DEBUG: gender_id={self.gender_id!r} (type={type(self.gender_id)}), "
                        f"environment_map keys={[ (k, type(k)) for k in getattr(gender_map, 'keys', lambda: [])() ]}"
                    )
                    print(debug_info)
                    message = f"Gender value {self.gender_id} is not in the gender map. Valid gender values are: {list(getattr(gender_map, 'keys', lambda: [])())}. Setting gender to None."
                    logging.warning(message)
                    raise ValueError(message)
            except TypeError:
                # If gender_map is a Mock or not iterable, skip this check
                pass
        self.date_of_birth = date_of_birth
        self.year_of_birth, self.age_min, self.age_max = self._resolve_birth_and_age_inputs(
            year_of_birth=year_of_birth,
            age=age,
            age_min=age_min,
            age_max=age_max,
            date_of_birth=date_of_birth,
        )
        if self.get_age() > 200:
            logging.warning(f"Age ({self.get_age()}) is unusually high.")

        if name is None:
            self.name = self._assign_name_from_ons(ons_male_file=ons_male_file, ons_female_file=ons_female_file)
        else:
            self.set_name(name)

        self.interests = {}
        self.opinions = {}
        self.values = {}
        # `base_traits` are mutable and can change during simulation (e.g., reflection).
        self.base_traits = {}
        # Backward-compatible alias used by existing code/tests.
        self.traits = self.base_traits
        self.trait_beliefs = TraitBeliefState()
        # Backward-compatible aliases.
        self.self_trait_opinions = self.trait_beliefs.self_trait_opinions
        self.other_trait_opinions = self.trait_beliefs.other_trait_opinions
        # If interests are provided, deep copy them to the person so that they have their own interests.
        if interests is not None:
            for interest_topic_id, interest in interests.items():
                self.interests[interest_topic_id] = copy.deepcopy(interest)
        # If opinions are provided, deep copy them to the person so that they have their own opinions.
        if opinions is not None:
            for opinion_topic_id, opinion in opinions.items():
                self.opinions[opinion_topic_id] = copy.deepcopy(opinion)
        # If values are provided, deep copy them to the person so that they have their own value priorities.
        if values is not None:
            for value_topic_id, value_obj in values.items():
                self.values[value_topic_id] = copy.deepcopy(value_obj)
        else:
            self.generate_values_profile(
                seed=value_seed,
                economic_security=value_economic_security,
                stochastic=value_stochastic,
                overwrite=True,
            )
        self._initialize_trait_state(traits)

    def _resolve_birth_and_age_inputs(
        self,
        year_of_birth: int | None,
        age: int | None,
        age_min: int | None,
        age_max: int | None,
        date_of_birth: date | None,
    ) -> tuple[int, int, int]:
        """Resolve supported age representations into canonical year + min/max age."""
        has_year = year_of_birth is not None
        has_age = age is not None
        has_range = age_min is not None or age_max is not None
        has_dob = date_of_birth is not None

        mode_count = sum([has_year, has_age, has_range, has_dob])
        if mode_count > 1:
            raise ValueError("Specify only one of year_of_birth, age, age range, or date_of_birth.")

        if has_dob:
            if not isinstance(date_of_birth, date):
                raise TypeError("date_of_birth must be a datetime.date instance.")
            resolved_age = self.environment.year - date_of_birth.year
            if resolved_age < 0:
                raise ValueError("date_of_birth cannot be in the future relative to environment year.")
            return date_of_birth.year, resolved_age, resolved_age

        if has_age:
            if age < 0:
                raise ValueError("age must be >= 0")
            resolved_year = self.environment.year - age
            return resolved_year, age, age

        if has_range:
            if age_min is None or age_max is None:
                raise ValueError("Both age_min and age_max must be provided when using an age range.")
            if age_min < 0 or age_max < 0:
                raise ValueError("age_min and age_max must be >= 0")
            if age_min > age_max:
                raise ValueError("age_min must be <= age_max")
            midpoint_age = (age_min + age_max) // 2
            resolved_year = self.environment.year - midpoint_age
            return resolved_year, age_min, age_max

        if not has_year:
            default_age = 18
            return self.environment.year - default_age, default_age, default_age

        resolved_year = year_of_birth
        if resolved_year > self.environment.year:
            logging.warning(
                "year_of_birth (%s) cannot be greater than the current year (%s). "
                "Setting year_of_birth to %s.",
                resolved_year,
                self.environment.year,
                self.environment.year,
            )
            resolved_year = self.environment.year
        resolved_age = self.environment.year - resolved_year
        if resolved_age < 0:
            resolved_age = 0
        return resolved_year, resolved_age, resolved_age

    @classmethod
    def _load_ons_table_cached(cls, csv_path: Path):
        resolved = Path(csv_path).resolve()
        table = cls._ons_table_cache.get(resolved)
        if table is None:
            table = load_ons_name_table(resolved)
            cls._ons_table_cache[resolved] = table
        return table

    def _sex_for_name_selection(self) -> str:
        gender_text = str(self.get_gender()).strip().lower()
        if "female" in gender_text:
            return "female"
        if "male" in gender_text:
            return "male"
        return "any"

    def _assign_name_from_ons(self, ons_male_file: Path = None, ons_female_file: Path = None) -> str:
        default_male, default_female = get_default_ons_name_paths()
        male_path = ons_male_file or default_male
        female_path = ons_female_file or default_female
        male_table = self._load_ons_table_cached(male_path)
        female_table = self._load_ons_table_cached(female_path)

        person_id_num = self.id.id if hasattr(self.id, "id") else int(self.id)
        gender_id_num = 0 if self.gender_id is None else self.gender_id.id
        birth_year_num = 0 if self.year_of_birth is None else self.year_of_birth
        seed = ((person_id_num * 1000003) + (gender_id_num * 101) + (birth_year_num * 9176) + self.environment.year) & 0xFFFFFFFF
        rng = random.Random(seed)
        return choose_name_for_person(
            rng=rng,
            male_table=male_table,
            female_table=female_table,
            sex=self._sex_for_name_selection(),
            birth_year=self.year_of_birth,
            used_names=None,
        )

    def set_name(self, name: str):
        """Set the person name."""
        if name is None:
            raise ValueError("name cannot be None")
        candidate = str(name).strip()
        if not candidate:
            raise ValueError("name cannot be empty")
        self.name = candidate

    def get_name(self) -> str:
        """Get the person name."""
        return self.name

    @classmethod
    def with_random_traits(
        cls,
        person_id: PersonID,
        environment: Environment,
        year_of_birth: int,
        gender_id: GenderID,
        age: int = None,
        age_min: int = None,
        age_max: int = None,
        date_of_birth: date = None,
        name: str = None,
        ons_male_file: Path = None,
        ons_female_file: Path = None,
        seed: int = None,
        topic_ids: list[TraitTopicID] = None,
        value_choices: list[int] = None,
        generate_interests: bool = False,
        interest_seed: int = None,
        generate_values: bool = False,
        value_seed: int = None,
        value_economic_security: str = "medium",
        value_stochastic: bool = True,
    ) -> "Person":
        """
        Build a Person pre-populated with a random trait profile.

        Args:
            person_id: Unique person identifier.
            environment: Simulation environment.
            year_of_birth: Person year of birth.
            gender_id: Person gender identifier.
            age: Optional exact age in years.
            age_min: Optional minimum age in years.
            age_max: Optional maximum age in years.
            date_of_birth: Optional full birth date.
            name: Optional display name for the person.
            ons_male_file: Optional path to ONS male names CSV for auto-assignment.
            ons_female_file: Optional path to ONS female names CSV for auto-assignment.
            seed: Optional deterministic seed for trait generation.
            topic_ids: Optional trait topics to generate. Defaults to Big Five.
            value_choices: Optional allowed trait values. Defaults to [-2,-1,0,1,2].
            generate_interests: If True, also generate default trait-guided interests.
            interest_seed: Optional deterministic seed for interest generation.
            generate_values: If True, regenerate values profile after creation.
            value_seed: Optional deterministic seed for values-profile generation.
            value_economic_security: Economic-security context for values profile.
            value_stochastic: If True, include stochastic jitter in values profile.

        Returns:
            A Person instance initialized with random traits.
        """
        random_traits = Trait.random_profile(
            seed=seed,
            topic_ids=topic_ids,
            value_choices=value_choices,
        )
        person = cls(
            person_id=person_id,
            environment=environment,
            year_of_birth=year_of_birth,
            gender_id=gender_id,
            age=age,
            age_min=age_min,
            age_max=age_max,
            date_of_birth=date_of_birth,
            name=name,
            ons_male_file=ons_male_file,
            ons_female_file=ons_female_file,
            traits=random_traits,
        )
        if generate_interests:
            person.generate_default_interests(seed=interest_seed)
        if generate_values:
            person.generate_values_profile(
                seed=value_seed,
                economic_security=value_economic_security,
                stochastic=value_stochastic,
                overwrite=True,
            )
        return person

    @staticmethod
    def _default_trait_description(value: int | float) -> str:
        if value <= -2:
            return "very low"
        if value == -1:
            return "low"
        if value == 0:
            return "neither high nor low"
        if value == 1:
            return "high"
        return "very high"

    def _build_trait(self, trait_topic_id: TraitTopicID, value: int | float, description: str = None) -> Trait:
        trait_description = description if description is not None else self._default_trait_description(value)
        trait_value = TraitValue(trait_topic_id, value, trait_description)
        return Trait(trait_topic_id, TraitValueMap({trait_topic_id: trait_value}), value)

    def _initialize_trait_state(self, traits: dict[TraitTopicID, 'Trait'] = None):
        # Ensure each person has canonical values for the Big Five traits.
        # Others can still provide additional custom traits.
        big_five_topic_ids = [
            TraitTopicID(0),  # Openness to experience
            TraitTopicID(1),  # Conscientiousness
            TraitTopicID(2),  # Extraversion
            TraitTopicID(3),  # Agreeableness
            TraitTopicID(4),  # Neuroticism
        ]
        provided_traits = traits or {}

        initial_trait_values = {}
        for topic_id in big_five_topic_ids:
            provided_trait = provided_traits.get(topic_id)
            initial_trait_values[topic_id] = 0 if provided_trait is None else provided_trait.value

        # Add custom traits while keeping the Big Five guaranteed.
        for topic_id, trait in provided_traits.items():
            if topic_id not in initial_trait_values:
                initial_trait_values[topic_id] = trait.value

        # Canonical initial values are immutable.
        self.initial_trait_values = MappingProxyType(initial_trait_values)

        # Mutable base trait objects start as a copy of canonical initial values.
        for topic_id, value in self.initial_trait_values.items():
            provided_trait = provided_traits.get(topic_id)
            provided_description = None if provided_trait is None else provided_trait.get_description()
            self.base_traits[topic_id] = self._build_trait(topic_id, value, provided_description)

    def __str__(self):
        """
        Return:
            String representation.
        """
        super_str = super().__str__()
        return f"{super_str}, year_of_birth={self.year_of_birth}, gender={self.get_gender()}, interests={self.interests}, opinions={self.opinions}"

    def get_age(self) -> int:
        """
        Get the age in years based on the current year in the environment.

        Return:
            Age in years, or None if year_of_birth is not set.
        """
        if self.year_of_birth is None:
            return None
        return self.environment.year - self.year_of_birth

    def get_age_range(self) -> tuple[int, int]:
        """
        Get the person's age bounds in years.

        Return:
            A tuple of (age_min, age_max).
        """
        return (self.age_min, self.age_max)

    def has_exact_age(self) -> bool:
        """
        Return whether this person has an exact known age.
        """
        return self.age_min == self.age_max

    def get_birthday_month_day(self) -> tuple[int, int] | None:
        """
        Get birthday month/day when a full date_of_birth is known.

        Return:
            (month, day) or None if no full date_of_birth is available.
        """
        if self.date_of_birth is None:
            return None
        return (self.date_of_birth.month, self.date_of_birth.day)

    def is_birthday(self, month: int, day: int) -> bool:
        """
        Return True when the given month/day matches this person's birthday.

        Args:
            month: Calendar month (1-12).
            day: Calendar day (1-31, validated against known date_of_birth).
        """
        if month < 1 or month > 12:
            raise ValueError("month must be in 1..12")
        if day < 1 or day > 31:
            raise ValueError("day must be in 1..31")
        birthday = self.get_birthday_month_day()
        if birthday is None:
            return False
        return birthday == (month, day)

    def get_gender(self) -> str:
        """
        Get the gender as a string.

        Return:
            Gender as a string.
        """
        if self.gender_id is None:
            return "none"
        gender_map = getattr(self.environment, 'gender_map', None)
        if gender_map is None:
            return str(self.gender_id)
        # Try to get the gender string, fallback to str(self.gender_id)
        try:
            gender = gender_map.get(self.gender_id)
            if hasattr(gender, 'description'):
                return gender.description
            if gender is not None:
                return str(gender)
        except Exception:
            pass
        return str(self.gender_id)

    def get_interest(self, interest_id: InterestTopicID) -> 'Interest':
        """
        Args:
            interest_id: The ID of the interest to get.
        Return:
            The Interest object for the interest_id, or None if not found.
        """
        return self.interests.get(interest_id)

    def get_value_priority(self, value_topic_id: ValueTopicID) -> 'Values':
        """
        Args:
            value_topic_id: The ID of the value topic to get.
        Return:
            The Values object for the topic, or None if not found.
        """
        return self.values.get(value_topic_id)

    def get_trait(self, trait_id: TraitTopicID) -> 'Trait':
        """
        Args:
            trait_id: The ID of the trait to get.
        Return:
            The Trait object for the trait_id, or None if not found.
        """
        return self.base_traits.get(trait_id)

    def get_initial_trait_value(self, trait_id: TraitTopicID) -> int:
        """
        Get the immutable canonical initial value for a trait.

        Args:
            trait_id: The trait topic ID.

        Return:
            The immutable initial trait value, or None if not present.
        """
        return self.initial_trait_values.get(trait_id)

    def set_base_trait_value(self, trait_id: TraitTopicID, value: int | float, description: str = None):
        """
        Update the mutable base trait value.

        Args:
            trait_id: The trait topic ID.
            value: The new mutable value.
            description: Optional description for the new value.
        """
        self.base_traits[trait_id] = self._build_trait(trait_id, value, description)

    def set_self_trait_opinion(self, trait_id: TraitTopicID, value: int | float):
        """
        Set this person's self-perceived value for a trait.
        """
        self.trait_beliefs.set_self_opinion(trait_id, value)

    def get_self_trait_opinion(self, trait_id: TraitTopicID) -> int | float:
        """
        Get this person's self-perceived value for a trait.
        """
        return self.trait_beliefs.get_self_opinion(trait_id)

    def set_other_trait_opinion(self,
        other_agent_id: int | AgentID,
        trait_id: TraitTopicID,
        value: int | float,
        order: int = 1):
        """
        Set this person's opinion about another person's trait value.

        :param other_agent_id: Other agent's ID.
        :param trait_id: Trait topic ID.
        :param value: Opinion value.
        :param order:
            1 for opinion of other's base trait, 2+ for higher-order opinions
            (for example, other's opinion of traits).
        """
        self.trait_beliefs.set_other_opinion(other_agent_id, trait_id, value, order)

    def get_other_trait_opinion(self,
        other_agent_id: int | AgentID,
        trait_id: TraitTopicID,
        order: int = 1) -> int | float:
        """
        Get this person's opinion about another person's trait value.

        Args:
            other_agent_id: Other agent's ID.
            trait_id: Trait topic ID.
            order: Recursion order of opinion.

        Return:
            Stored opinion value, or None if not found.
        """
        return self.trait_beliefs.get_other_opinion(other_agent_id, trait_id, order)

    def export_trait_state(self) -> dict:
        """
        Export trait state for reproducible checkpoints.

        Returns:
            A serializable dictionary containing immutable initial values,
            mutable base trait values, and trait beliefs.
        """
        return {
            "initial_trait_values": {
                trait_id.id: value for trait_id, value in self.initial_trait_values.items()
            },
            "base_traits": {
                trait_id.id: trait.value for trait_id, trait in self.base_traits.items()
            },
            "trait_beliefs": self.trait_beliefs.to_dict(),
        }

    def import_trait_state(self, state: dict):
        """
        Import trait state from a dictionary produced by export_trait_state().
        """
        initial_values = {
            TraitTopicID(int(trait_id)): value
            for trait_id, value in state.get("initial_trait_values", {}).items()
        }
        if initial_values:
            self.initial_trait_values = MappingProxyType(initial_values)

        imported_base_traits = {}
        for trait_id, value in state.get("base_traits", {}).items():
            topic_id = TraitTopicID(int(trait_id))
            imported_base_traits[topic_id] = self._build_trait(topic_id, value)
        if imported_base_traits:
            self.base_traits = imported_base_traits
            self.traits = self.base_traits

        self.trait_beliefs = TraitBeliefState.from_dict(state.get("trait_beliefs", {}))
        self.self_trait_opinions = self.trait_beliefs.self_trait_opinions
        self.other_trait_opinions = self.trait_beliefs.other_trait_opinions

    def reflect_on_traits(self,
        learning_rate: float = 0.25,
        clamp_min: float = -2,
        clamp_max: float = 2,
        seed: int = None):
        """
        Update mutable base traits by reflecting towards self-perceived trait opinions.

        Args:
            learning_rate: Fractional adjustment towards self-opinion.
            clamp_min: Minimum value after update.
            clamp_max: Maximum value after update.
            seed: Optional deterministic seed for tie/noise resolution.
        """
        if learning_rate < 0:
            raise ValueError("learning_rate must be >= 0")

        rng = random if seed is None else random.Random(seed)
        for trait_id, trait in self.base_traits.items():
            perceived = self.get_self_trait_opinion(trait_id)
            if perceived is None:
                continue
            delta = (perceived - trait.value) * learning_rate
            jitter = rng.uniform(-1e-9, 1e-9)
            updated = trait.value + delta + jitter
            updated = max(clamp_min, min(clamp_max, updated))
            self.set_base_trait_value(trait_id, updated)

    def generate_interests_from_traits(self,
        seed: int = None,
        total_interest_topics: int = 9,
        overwrite: bool = False,
        interest_topics: dict[InterestTopicID, InterestTopic] = None) -> dict[InterestTopicID, 'Interest']:
        """
        Generate interests influenced by traits.

        The openness-to-experience trait (TraitTopicID(0)) influences how many
        interests are generated: higher openness leads to more interests.

        :param seed:
            Optional seed for deterministic generation. If ``None``, the global
            random module state is used.
        :param total_interest_topics:
            Number of available interest topics to sample from.
        :param overwrite:
            If ``True``, replace existing interests. If ``False`` and interests
            already exist, leave them unchanged.
        :param interest_topics:
            Optional topic catalog to sample from. If provided, topic IDs in this
            dictionary are used instead of synthesizing IDs from
            ``total_interest_topics``.
        :return:
            The person's interest dictionary.
        """
        if len(self.interests) > 0 and not overwrite:
            return self.interests

        if total_interest_topics <= 0:
            self.interests = {}
            return self.interests

        if interest_topics is not None:
            available_topic_ids = sorted(interest_topics.keys(), key=lambda topic_id: topic_id.id)
        else:
            default_topic_ids = InterestTopic.default_topic_ids()
            if total_interest_topics <= len(default_topic_ids):
                available_topic_ids = default_topic_ids[:total_interest_topics]
            else:
                available_topic_ids = list(default_topic_ids)
                for topic_id in range(len(default_topic_ids), total_interest_topics):
                    available_topic_ids.append(InterestTopicID(topic_id))

        if len(available_topic_ids) == 0:
            self.interests = {}
            return self.interests

        openness_topic_id = TraitTopicID(0)
        openness_trait = self.base_traits.get(openness_topic_id)
        openness_value = 0 if openness_trait is None else openness_trait.value

        # Map openness to number of interests so higher openness yields more topics.
        if openness_value >= 2:
            target_count = 7
        elif openness_value == 1:
            target_count = 6
        elif openness_value == 0:
            target_count = 4
        elif openness_value == -1:
            target_count = 3
        else:
            target_count = 2

        target_count = max(1, min(target_count, len(available_topic_ids)))
        rng = random if seed is None else random.Random(seed)
        topic_ids = rng.sample(available_topic_ids, k=target_count)

        if openness_value >= 1:
            interest_value_choices = [1, 2]
        elif openness_value <= -1:
            interest_value_choices = [0, 1]
        else:
            interest_value_choices = [0, 1, 2]

        descriptions = {
            0: "occasionally interested",
            1: "interested",
            2: "very interested",
        }

        generated_interests = {}
        for interest_topic_id in topic_ids:
            interest_value = rng.choice(interest_value_choices)
            interest_value_obj = InterestValue(interest_topic_id, interest_value, descriptions[interest_value])
            generated_interests[interest_topic_id] = Interest(
                interest_topic_id,
                InterestValueMap.default_for_topic(
                    interest_topic_id,
                    value=interest_value_obj.value,
                    description=interest_value_obj.description,
                ),
                interest_value,
            )

        self.interests = generated_interests
        return self.interests

    def generate_default_interests(
        self,
        seed: int = None,
        overwrite: bool = False,
    ) -> dict[InterestTopicID, 'Interest']:
        """
        Convenience wrapper to generate trait-guided interests from default topics.

        Args:
            seed: Optional deterministic seed.
            overwrite: If True, replace existing interests.

        Returns:
            The person's interest dictionary.
        """
        default_topics = InterestTopic.default_topics()
        return self.generate_interests_from_traits(
            seed=seed,
            overwrite=overwrite,
            total_interest_topics=len(default_topics),
            interest_topics=default_topics,
        )

    def generate_values_profile(
        self,
        seed: int = None,
        economic_security: str = "medium",
        stochastic: bool = True,
        overwrite: bool = False,
    ) -> dict[ValueTopicID, 'Values']:
        """
        Generate value priorities informed by demographic and economic context.

        Args:
            seed: Optional deterministic seed.
            economic_security: One of "low", "medium", "high".
            stochastic: If True, include small random variation.
            overwrite: If True, replace existing values.

        Return:
            The person's value-priority dictionary.
        """
        if len(self.values) > 0 and not overwrite:
            return self.values

        gender = self.get_gender()
        if gender in {"none", "unknown"}:
            gender = None

        self.values = Values.default_profile(
            seed=seed,
            age=self.get_age(),
            gender=gender,
            economic_security=economic_security,
            stochastic=stochastic,
        )
        return self.values

    def get_opinion(self, opinion_id: OpinionTopicID) -> 'Opinion':
        """
        Args:
            opinion_id: The ID of the opinion to get.
        Return:
            The Opinion object for the opinion_id, or None if not found.
        """
        return self.opinions.get(opinion_id)
    
    def add_interest(self, interest: 'Interest', value: InterestValue):
        """
        Add interest to interests.

        Args:
            interest: The Interest to add.
            value: The InterestValue to add for the interest.
        """
        self.interests[interest.interest_id] = interest
        self.interests[interest.interest_id].value = value

    def add_opinion(self, opinion: 'Opinion', value: OpinionValue):
        """
        Add opinion to opinions.

        Args:
            opinion: The Opinion to add.
            value: The OpinionValue to add for the opinion.
        """
        self.opinions[opinion.opinion_id] = opinion
        self.opinions[opinion.opinion_id].value = value

    def set_interest(self, interest_id: InterestTopicID, value: InterestValue):
        """
        Set an interest value.

        Args:
            interest_id: The ID of the interest to set.
            value: The value to set the interest to.
        """
        if interest_id not in self.interests:
            message = (f"Attempting to set interest value for non-existent interest ID {interest_id}. "
                       f"Valid interest IDs are: {list(self.interests.keys())}. "
                       f"Adding new interest with value {value}.")
            logging.warning(message)
            raise ValueError(message)
        else:
            self.interests[interest_id].value = value

    def set_opinion(self, opinion_id: OpinionTopicID, value: OpinionValue):
        """
        Set an opinion value.

        Args:
            opinion_id: The ID of the opinion to set.
            value: The value to set the opinion to.
        """
        if opinion_id not in self.opinions:
            message = (f"Attempting to set opinion value for non-existent opinion ID {opinion_id}. "
                       f"Valid opinion IDs are: {list(self.opinions.keys())}. "
                       f"Adding new opinion with value {value}.")
            logging.warning(message)
            raise ValueError(message)
        else:
            self.opinions[opinion_id].value = value

    def get_interest_profile(self) -> str:
        """
        An interest profile is a summary of interests reflecting the similarity and difference 
        in interests of the individual relative to their groups and others in the enviornment.
        
        Return:
            A string summarizing the interest profile.
        """
        if len(self.interests) == 0:
            return "I have no interests."
        # Return a simple summary what the interests are.
        summary = "I have interests in the following topics:\n"
        for topic, value in self.interests.items():
            summary += f"  {topic}\n"
        return summary

    def get_opinion_profile(self) -> str:
        """
        An opinion profile is a summary of opinions reflecting the similarity and difference 
        in opinions of the individual relative to their groups and others in the enviornment.
        
        Return:
            A string summarizing the opinion profile.
        """
        if len(self.opinions) == 0:
            return "I have no opinions."
        # Return a simple summary what the opinions are.
        summary = "I have opinions about the following topics:\n"
        for topic, value in self.opinions.items():
            summary += f"  {topic}\n"
        return summary

    def get_self_description(self) -> str:
        """
        Get a self-description of the person.

        Return:
            A string describing the person.
        """
        if self.has_exact_age():
            age = self.get_age()
            desc = f"I am {age} years old. "
        else:
            desc = f"I am between {self.age_min} and {self.age_max} years old. "
        if self.gender_id is not None:
            desc += f"I am {self.get_gender()}. "
        if getattr(self, "name", None):
            desc += f"My name is {self.name}. "
        return desc

    def communicate(self, i: int):
        """
        Communicate with another agent.

        Args:
            i: The index of the agent to communicate with.
        Note:
            This method should only be used when both self and the other agent are instances of Person
            (i.e., have 'interests' and 'opinions' attributes). If not, the method will log a warning and do nothing.
        """
        other_agent = self.environment.agents_active[i]
        if not isinstance(other_agent, Person):
            logging.warning(f"communicate called with non-Person agent: {type(other_agent)}. Skipping communication.")
            return
        if not (hasattr(self, 'interests') and hasattr(other_agent, 'interests')):
            logging.warning(f"communicate called with non-Person agent(s): self={type(self)}, other_agent={type(other_agent)}. Skipping communication.")
            return
        if not (hasattr(self, 'opinions') and hasattr(other_agent, 'opinions')):
            logging.warning(f"communicate called with non-Person agent(s): self={type(self)}, other_agent={type(other_agent)}. Skipping communication.")
            return
        logging.info(f"{self} is communicating with {other_agent}")
        # If either agent is in the Neutral group, update the neutral agents opinions to the average
        neutral_groups = [group for group in self.environment.groups_active.values() if group.name == "Neutral"]
        self_in_neutral = any(self in group.members for group in neutral_groups)
        other_in_neutral = any(other_agent in group.members for group in neutral_groups)
        if self_in_neutral or other_in_neutral:
            # Build averaged opinions for all topics
            avg_opinions = {}
            for topic in set(self.opinions.keys()).union(other_agent.opinions.keys()):
                self_opinion = self.opinions.get(topic, None)
                other_opinion = other_agent.opinions.get(topic, None)
                self_val = self_opinion.value if self_opinion is not None else 0
                other_val = other_opinion.value if other_opinion is not None else 0
                avg_value = int(round((self_val + other_val) / 2))
                # Use self's opinion_values if available, else other's, else None
                opinion_values = None
                if self_opinion is not None:
                    opinion_values = self_opinion.opinion_values
                elif other_opinion is not None:
                    opinion_values = other_opinion.opinion_values
                else:
                    opinion_values = None
                avg_opinions[topic] = Opinion(topic, opinion_values, avg_value)
            if self_in_neutral:
                self.opinions = {topic: opinion for topic, opinion in avg_opinions.items()}
                logging.info(f"{self} is in the Neutral group, so opinion is updated to the average of { {k: v.value for k, v in avg_opinions.items()} }")
            if other_in_neutral:
                other_agent.opinions = {topic: opinion for topic, opinion in avg_opinions.items()}
                logging.info(f"{other_agent} is in the Neutral group, so opinion is updated to the average of { {k: v.value for k, v in avg_opinions.items()} }")
    
    def get_persona(self) -> str:
        """
        Compile and return a persona as a string based on demographics and values.
        """
        return self.get_self_description().strip()
    
    def get_interests_summary(self) -> str:
        """
        Compile and return a summary of interests as a string.
        """
        if not self.interests:
            return "I have no interests."

        def _join_topics(topic_names: list[str]) -> str:
            if len(topic_names) == 1:
                return topic_names[0]
            if len(topic_names) == 2:
                return f"{topic_names[0]} and {topic_names[1]}"
            return ", ".join(topic_names[:-1]) + f", and {topic_names[-1]}"

        default_topics = InterestTopic.default_topics()
        entries = []
        for interest in self.interests.values():
            topic = default_topics.get(interest.id)
            topic_name = topic.topic if topic is not None else str(interest.id)
            entries.append((interest.id.id, topic_name, interest.value))

        # Keep deterministic ordering for summaries.
        entries.sort(key=lambda item: item[0])
        values = [value for _, _, value in entries]

        if all(value == 0 for value in values):
            return "I don't currently have any interests."

        most_interested_value = 2 if 2 in values else (1 if 1 in values else None)
        most_disinterested_value = -2 if -2 in values else (-1 if -1 in values else None)

        parts = []
        if most_interested_value is not None:
            interested_topics = [topic_name for _, topic_name, value in entries if value == most_interested_value]
            parts.append(f"I am interested in {_join_topics(interested_topics)}.")

        if most_disinterested_value is not None:
            disinterested_topics = [topic_name for _, topic_name, value in entries if value == most_disinterested_value]
            parts.append(f"I am not interested in {_join_topics(disinterested_topics)}.")

        if not parts:
            return "I'm not sure what I am interested in."
        return " ".join(parts)

    def get_values_summary(self) -> str:
        """
        Compile and return a summary of value priorities as a string.
        """
        if not self.values:
            return ""

        def _join_topics(topic_names: list[str]) -> str:
            if len(topic_names) == 1:
                return topic_names[0]
            if len(topic_names) == 2:
                return f"{topic_names[0]} and {topic_names[1]}"
            return ", ".join(topic_names[:-1]) + f", and {topic_names[-1]}"

        # Build deterministic entries by topic ID.
        topic_lookup = {}
        from gabm.abm.attributes.values import ValueTopic
        for topic_id, topic in ValueTopic.default_topics().items():
            topic_lookup[topic_id] = topic.topic

        entries = []
        for value_obj in self.values.values():
            topic_name = topic_lookup.get(value_obj.id, str(value_obj.id))
            entries.append((value_obj.id.id, topic_name, value_obj.value))
        entries.sort(key=lambda item: item[0])

        priorities = [priority for _, _, priority in entries]
        if len(set(priorities)) == 1:
            return ""

        max_priority = max(priorities)
        min_priority = min(priorities)

        top_topics = [topic_name for _, topic_name, priority in entries if priority == max_priority]
        low_topics = [topic_name for _, topic_name, priority in entries if priority == min_priority]

        return (
            f"I value {_join_topics(top_topics)}."
        )
 
    def communicate_with_llm(self, message: str, model: str = None) -> dict:
        """
        Communicate with an LLM to get a response based on the input message and model.
        
        Args:
            message: The prompt to send to the LLM.
            model: The name of the LLM model to use (optional).
        Return:
            The response from the LLM as a dictionary, or None if an error occurs
        """
        # For now, we will just return a dummy response.
        # In the future, this method can be implemented to call an actual LLM API.
        return {"response": f"Echo: {message}", "model": model}

class CitizenID(PersonID):
    """
    Citizen ID
    """
    def __init__(self, agent_id: int):
        """
        Initialize.

        Args:
            agent_id: Unique identifier for the Citizen instance.
        """
        super().__init__(agent_id)

class Citizen(Person):
    """
    A Person who belongs to a Nation.

    .. note::
        Inherits all attributes from :class:`Person`.

    Attributes:
        region_id (RegionID):
            The agent's region, represented as a RegionID.
        education_id (EducationID):
            The agent's education level, represented as an EducationID.
        ethnicity_id (EthnicityID):
            The agent's ethnicity, represented as an EthnicityID.
        employment_id (EmploymentID):
            The agent's employment status, represented as an EmploymentID.
        income_id (IncomeID):
            The agent's income level, represented as an IncomeID.
    """
    def __init__(self, citizen_id: CitizenID, nation: Nation,
        year_of_birth: int = None,
        age: int = None,
        age_min: int = None,
        age_max: int = None,
        date_of_birth: date = None,
        gender_id: GenderID = None,
        name: str = None,
        traits: dict = None,
        opinions: dict = None,
        interests: dict = None,
        ons_male_file: Path = None,
        ons_female_file: Path = None,
        region_id: int = None,
        education_id: int = None,
        ethnicity_id: int = None,
        employment_id: int = None,
        income_id: int = None):
        """
        Initialize.

        Args:
            citizen_id (AgentID):
                Unique identifier for the citizen.
            environment (Nation):
                The Nation the citizen belongs to.
            year_of_birth (int):
                Year of birth.
            age (int):
                Optional exact age in years.
            age_min (int):
                Optional minimum age in years.
            age_max (int):
                Optional maximum age in years.
            date_of_birth (date):
                Optional full birth date.
            gender_id (GenderID):
                The ID of the gender attributed.
            name (str):
                Optional display name for the citizen.
            traits (dict):
                A dictionary of traits, where keys are TraitTopicIDs and values are Trait objects.
            interests (dict):
                A dictionary of interests, where keys are InterestTopicIDs and values are Interest objects.
            opinions (dict):
                A dictionary of opinions, where keys are OpinionTopicIDs and values are Opinion objects.
            ons_male_file (Path):
                Optional path to ONS male names CSV used for auto-naming.
            ons_female_file (Path):
                Optional path to ONS female names CSV used for auto-naming.
            region_id (RegionID):
                The Id RegionID.
            education_id (EducationID):
                The agent's education level, represented as an EducationID.
            ethnicity_id (EthnicityID):
                The agent's ethnicity, represented as an EthnicityID.
            employment_id (EmploymentID):
                The agent's employment status, represented as an EmploymentID.
            income_id (IncomeID):
                The agent's income level, represented as an IncomeID.
        """
        super().__init__(person_id=citizen_id, environment=nation,
            year_of_birth=year_of_birth, gender_id=gender_id,
            age=age, age_min=age_min, age_max=age_max, date_of_birth=date_of_birth,
            name=name,
            traits=traits, interests=interests, opinions=opinions,
            ons_male_file=ons_male_file,
            ons_female_file=ons_female_file)
        self.region_id=region_id
        self.education_id=education_id
        self.ethnicity_id=ethnicity_id
        self.employment_id=employment_id
        self.income_id=income_id
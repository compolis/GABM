"""ONS-backed given-name loading and sampling helpers for agent naming."""

import csv
import random
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ONSNameTable:
    """Container for a single ONS name table."""

    names: list[str]
    year_to_ranked_names: dict[int, list[str]]

    @property
    def min_year(self) -> int:
        return min(self.year_to_ranked_names) if self.year_to_ranked_names else 0

    @property
    def max_year(self) -> int:
        return max(self.year_to_ranked_names) if self.year_to_ranked_names else 0


def get_default_ons_name_paths() -> tuple[Path, Path]:
    """Return default male/female ONS CSV paths from repository data/input/abm."""
    repo_root = Path(__file__).resolve().parents[4]
    male = repo_root / "data" / "input" / "abm" / "names_england_wales_ons_male.csv"
    female = repo_root / "data" / "input" / "abm" / "names_england_wales_ons_female.csv"
    return male, female


def load_ons_name_table(csv_path: Path) -> ONSNameTable:
    """Load one ONS CSV and return names plus per-year ranked name lists."""
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))

    header_idx = None
    for idx, row in enumerate(rows):
        if row and row[0].strip() == "Name":
            header_idx = idx
            break

    if header_idx is None:
        raise ValueError(f"Could not find 'Name' header row in {csv_path}")

    header_row = rows[header_idx]
    names = [cell.strip() for cell in header_row[1:] if cell.strip()]
    year_to_ranked_names: dict[int, list[str]] = {}

    for row in rows[header_idx + 1 :]:
        if not row:
            continue
        year_cell = row[0].strip()
        if not year_cell.isdigit():
            continue

        year = int(year_cell)
        rank_and_name: list[tuple[int, str]] = []
        for name, value in zip(names, row[1:]):
            rank_cell = value.strip()
            if rank_cell.isdigit():
                rank_and_name.append((int(rank_cell), name))

        if rank_and_name:
            rank_and_name.sort(key=lambda item: (item[0], item[1]))
            year_to_ranked_names[year] = [name for _, name in rank_and_name]

    return ONSNameTable(names=names, year_to_ranked_names=year_to_ranked_names)


def get_names_for_birth_year(table: ONSNameTable, birth_year: int | None) -> list[str]:
    """Return ranked names for a birth year, clamped to available ONS years."""
    if not table.year_to_ranked_names:
        return list(table.names)

    if birth_year is None:
        return list(table.names)

    year = max(table.min_year, min(table.max_year, birth_year))
    return list(table.year_to_ranked_names.get(year, table.names))


def _dedupe_preserve_order(names: list[str]) -> list[str]:
    """Return deduplicated names preserving first-seen order."""
    seen: set[str] = set()
    out: list[str] = []
    for name in names:
        if name not in seen:
            seen.add(name)
            out.append(name)
    return out


def choose_name_for_person(
    rng: random.Random,
    male_table: ONSNameTable,
    female_table: ONSNameTable,
    sex: str,
    birth_year: int | None,
    used_names: set[str] | None = None,
) -> str:
    """Choose one deterministic name based on sex and approximate birth year."""
    sex_norm = (sex or "any").strip().lower()

    if sex_norm == "male":
        pool = get_names_for_birth_year(male_table, birth_year)
    elif sex_norm == "female":
        pool = get_names_for_birth_year(female_table, birth_year)
    else:
        male_pool = get_names_for_birth_year(male_table, birth_year)
        female_pool = get_names_for_birth_year(female_table, birth_year)
        pool = _dedupe_preserve_order(male_pool + female_pool)

    if used_names:
        pool = [name for name in pool if name not in used_names]

    if not pool:
        pool = _dedupe_preserve_order(male_table.names + female_table.names)

    return rng.choice(pool)

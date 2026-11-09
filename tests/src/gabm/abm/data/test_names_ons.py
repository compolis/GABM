"""Tests for ONS-backed name loading and selection helpers in ABM data."""

from pathlib import Path
import random

from gabm.abm.data.names_ons import (
    choose_name_for_person,
    get_default_ons_name_paths,
    get_names_for_birth_year,
    load_ons_name_table,
)


def test_load_ons_name_table_finds_name_header_and_year_rows(tmp_path):
    """Loader should ignore metadata lines and parse Name + year rows."""
    csv_path = tmp_path / "mini_ons.csv"
    csv_path.write_text(
        "Title line,,,,\n"
        "Another header,,,,\n"
        "Name,Alex,Jordan,Sam\n"
        "2025,1,2,3\n"
        "2024,2,1,3\n",
        encoding="utf-8",
    )

    table = load_ons_name_table(csv_path)

    assert table.names == ["Alex", "Jordan", "Sam"]
    assert table.year_to_ranked_names[2025] == ["Alex", "Jordan", "Sam"]
    assert table.year_to_ranked_names[2024] == ["Jordan", "Alex", "Sam"]


def test_get_names_for_birth_year_clamps_to_available_year_range():
    """Birth years outside the available range should clamp to min/max year."""
    male_path, _ = get_default_ons_name_paths()
    table = load_ons_name_table(male_path)

    older = get_names_for_birth_year(table, 1900)
    newer = get_names_for_birth_year(table, 2100)

    assert older == table.year_to_ranked_names[table.min_year]
    assert newer == table.year_to_ranked_names[table.max_year]


def test_choose_name_for_person_uses_sex_specific_table_and_birth_year():
    """Selection should come from sex-specific pool for the clamped birth-year list."""
    male_path, female_path = get_default_ons_name_paths()
    male_table = load_ons_name_table(male_path)
    female_table = load_ons_name_table(female_path)

    rng = random.Random(42)
    female_name = choose_name_for_person(
        rng,
        male_table=male_table,
        female_table=female_table,
        sex="female",
        birth_year=2010,
        used_names=None,
    )

    female_pool = set(get_names_for_birth_year(female_table, 2010))
    assert female_name in female_pool


def test_choose_name_for_person_unknown_sex_draws_from_combined_pool():
    """Unknown sex should use a combined male+female pool."""
    male_path, female_path = get_default_ons_name_paths()
    male_table = load_ons_name_table(male_path)
    female_table = load_ons_name_table(female_path)

    rng = random.Random(1)
    name = choose_name_for_person(
        rng,
        male_table=male_table,
        female_table=female_table,
        sex="unknown",
        birth_year=2008,
        used_names=None,
    )

    combined_pool = set(get_names_for_birth_year(male_table, 2008) + get_names_for_birth_year(female_table, 2008))
    assert name in combined_pool


def test_get_default_ons_name_paths_exist():
    """Default ONS male/female CSV paths should exist in repository data/input/abm."""
    male_path, female_path = get_default_ons_name_paths()

    assert isinstance(male_path, Path)
    assert isinstance(female_path, Path)
    assert male_path.exists()
    assert female_path.exists()

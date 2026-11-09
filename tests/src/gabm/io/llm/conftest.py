from pathlib import Path

import pytest


@pytest.fixture
def api_keys():
    file_path = Path("data/api_key.csv")
    if not file_path.is_file():
        pytest.skip("API key file data/api_key.csv not found.")
    from gabm.io.read_data import read_api_keys

    return read_api_keys(file_path)

"""
Script to sync requirements.txt with install_requires in setup.cfg and/or dependencies in pyproject.toml.
Ensures PyPI packaging always uses up-to-date runtime dependencies.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Standard library imports
import configparser
from pathlib import Path
import sys
# Third-party imports
import tomlkit

ROOT = Path(__file__).parent.parent
REQ_TXT = ROOT / "requirements.txt"
SETUP_CFG = ROOT / "setup.cfg"
PYPROJECT = ROOT / "pyproject.toml"

# Read requirements.txt
with open(REQ_TXT, encoding="utf-8") as f:
    reqs = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Update setup.cfg if present (robust INI update)
if SETUP_CFG.exists():
    config = configparser.ConfigParser()
    config.optionxform = str  # preserve case
    config.read(SETUP_CFG)
    if 'options' not in config:
        config['options'] = {}
    # Indent each requirement for correct format
    config['options']['install_requires'] = '\n' + '\n'.join(f'    {r}' for r in reqs)
    with open(SETUP_CFG, 'w', encoding='utf-8') as f:
        config.write(f)
    print(f"Updated install_requires in {SETUP_CFG}")


# Update pyproject.toml if present (preserve formatting with tomlkit)
if PYPROJECT.exists():
    with open(PYPROJECT, encoding="utf-8") as f:
        pyproject_doc = tomlkit.parse(f.read())
    if "project" not in pyproject_doc:
        print(f"[project] section missing in {PYPROJECT}", file=sys.stderr)
        sys.exit(1)
    # Replace dependencies array, preserving formatting
    pyproject_doc["project"]["dependencies"] = tomlkit.array(reqs)
    with open(PYPROJECT, 'w', encoding='utf-8') as f:
        f.write(tomlkit.dumps(pyproject_doc))
    print(f"Updated dependencies in {PYPROJECT}")

print("Requirements sync complete.")

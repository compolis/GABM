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
import re

ROOT = Path(__file__).parent.parent
REQ_TXT = ROOT / "requirements.txt"
SETUP_CFG = ROOT / "setup.cfg"
PYPROJECT = ROOT / "pyproject.toml"

# Read requirements.txt
with open(REQ_TXT, encoding="utf-8") as f:
    reqs = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Update setup.cfg if present
if SETUP_CFG.exists():
    config = configparser.ConfigParser()
    config.read(SETUP_CFG)
    if 'options' not in config:
        config['options'] = {}
    config['options']['install_requires'] = '\n' + '\n'.join(reqs)
    with open(SETUP_CFG, 'w', encoding='utf-8') as f:
        config.write(f)
    print(f"Updated install_requires in {SETUP_CFG}")

# Update pyproject.toml if present
if PYPROJECT.exists():
    with open(PYPROJECT, encoding="utf-8") as f:
        pyproject = f.read()
    # Replace [project] dependencies = [...]
    new_deps = '\n'.join([f'    "{r}",' for r in reqs])
    pyproject_new = re.sub(
        r'(\[project\][^\[]*?dependencies\s*=\s*\[)[^\]]*?(\])',
        lambda m: m.group(1) + '\n' + new_deps + '\n' + m.group(2),
        pyproject,
        flags=re.DOTALL
    )
    with open(PYPROJECT, 'w', encoding='utf-8') as f:
        f.write(pyproject_new)
    print(f"Updated dependencies in {PYPROJECT}")

print("Requirements sync complete.")

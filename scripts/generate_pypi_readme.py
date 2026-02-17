
"""
Script to generate a PyPI-friendly README.md by extracting key sections from README.md and USER_GUIDE.md.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.2.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

import re
from pathlib import Path

# Paths
ROOT = Path(__file__).parent.parent
README_SRC = ROOT / "README.md"
USER_GUIDE = ROOT / "USER_GUIDE.md"
PYPI_README = ROOT / "README-pypi.md"

def extract_section(text, header, next_headers=None):
    """Extract a markdown section by header name."""
    if not next_headers:
        next_headers = ["## ", "# "]
    pattern = rf"## {re.escape(header)}(.*?)(?:(?:{'|'.join(map(re.escape, next_headers))})|\Z)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""

def extract_overview(readme):
    match = re.search(r"## Overview\n(.+?)(?:\n## |\Z)", readme, re.DOTALL)
    return match.group(1).strip() if match else ""

def extract_acknowledgements(readme):
    match = re.search(r"## Acknowledgements\n(.+?)(?:\n## |\Z)", readme, re.DOTALL)
    return match.group(1).strip() if match else ""

def extract_installation(user_guide):
    match = re.search(r"## Getting Started(.+?)(?:## |\Z)", user_guide, re.DOTALL)
    return match.group(1).strip() if match else ""

def extract_quick_example(user_guide):
    # Look for Example Usage code block
    match = re.search(r"Example Usage.*?```python(.*?)```", user_guide, re.DOTALL | re.IGNORECASE)
    if match:
        return f"```python\n{match.group(1).strip()}\n```"
    return ""

def extract_features(readme):
    # Optionally extract a features section if present
    match = re.search(r"## Features\n(.+?)(?:\n## |\Z)", readme, re.DOTALL)
    return match.group(1).strip() if match else ""

def main():
    with open(README_SRC, encoding="utf-8") as f:
        readme = f.read()
    with open(USER_GUIDE, encoding="utf-8") as f:
        user_guide = f.read()

    overview = extract_overview(readme)
    install = extract_installation(user_guide)
    quick_example = extract_quick_example(user_guide)
    features = extract_features(readme)
    acknowledgements = extract_acknowledgements(readme)

    # Extract badges block from README.md (first HTML block or <!-- Badges -->)
    badges_match = re.search(r"<!-- Badges -->(.*?</p>)", readme, re.DOTALL | re.IGNORECASE)
    badges = badges_match.group(0).strip() + "\n" if badges_match else ""

    # Read API_KEYS.md and extract a summary (first 20 lines or up to first code block)
    API_KEYS_MD = ROOT / "API_KEYS.md"

    try:
        with open(API_KEYS_MD, encoding="utf-8") as f:
            api_keys_md = f.read()
        # Extract up to first code block or 20 lines, skipping the first heading
        api_keys_lines = api_keys_md.splitlines()
        api_keys_summary = []
        for line in api_keys_lines[1:]:
            if line.strip().startswith("#"):
                continue  # skip any further headings
            if line.strip().startswith("```"):
                break
            api_keys_summary.append(line)
        api_keys_section = "\n".join(api_keys_summary).strip()
    except Exception:
        api_keys_section = "API key setup required."

    # Remove stray heading markers from api_keys_section
    api_keys_section_clean = re.sub(r"^#+ ", "", api_keys_section, flags=re.MULTILINE)
    # Remove the security warning blockquote if present (multi-line)
    api_keys_section_clean = re.sub(r"> \*\*Security Warning:.*?(?:\n(?!\S)|$)+", "", api_keys_section_clean, flags=re.DOTALL)

    # Only include Installation section if install is not empty or just a stray '#'
    install_block = install.strip()
    show_install = install_block and install_block != "#"

    pypi_readme = f"""
{badges}# GABM: Generative Agent-Based Model

{overview}

## Features
{features if features else '- Flexible, extensible agent-based modeling with LLMs\n- Multi-provider LLM support\n- Persistent response caching'}

## API Keys
{api_keys_section_clean}
"""
    if show_install:
        pypi_readme += f"""
## Installation
{install_block}
"""
    pypi_readme += f"""
## Quick Example
{quick_example if quick_example else '```python\nimport gabm\n# See documentation for usage examples\n```'}

## Documentation
Full documentation: https://compolis.github.io/GABM/

## Acknowledgements
{acknowledgements}
"""

    with open(PYPI_README, "w", encoding="utf-8") as f:
        f.write(pypi_readme.strip() + "\n")
    print(f"Generated {PYPI_README}")

if __name__ == "__main__":
    main()

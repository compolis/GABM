# Requirements (Developer)

> **Note:** This file is for documentation only.
> Install dependencies from [requirements.txt](requirements.txt) and [requirements-dev.txt](requirements-dev.txt) in the project root.


```# Development requirements for GABM
# Install with: pip install -r requirements-dev.txt

# Test dependencies
pytest>=9.0.2,<10

# LLM API dependencies
openai>=2.21.0,<3
#anthropic>=0.25.6,<0.26
google-generativeai>=0.4.1,<0.5
httpx>=0.28.1,<0.29
deepseek>=1.0.0,<2

# Dependencies for Apertus
transformers>=5.1.0,<6
torch>=2.10.0,<3

# Documentation dependencies
sphinx>=9.1.0,<10
sphinx-rtd-theme>=3.1.0,<4
myst-parser>=5.0.0,<6
docutils>=0.22,<0.23

# For building distributions
build>=1.4.0,<2
setuptools>=61.0,<70
wheel>=0.42.0,<1
toml>=0.10.2,<2

# For updating version references in files
bump2version>=1.0.1,<2

# For uploading to PyPI
twine>=5.0.0,<6
```
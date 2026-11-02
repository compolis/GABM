#!/usr/bin/env python3
"""
Platform-agnostic build and test install script for GABM.
- Builds the package (wheel and sdist)
- Creates a fresh virtual environment
- Installs the built wheel
- Imports gabm to verify install
- (Optional) Runs 'python -m gabm --help' to check entry point
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import os
import sys
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
VENV = ROOT / "venv-build-test"
PYTHON = sys.executable

# Clean up old venv and dist
if VENV.exists():
    shutil.rmtree(VENV)
if DIST.exists():
    shutil.rmtree(DIST)

# Build the package
print("Building the package...")
subprocess.check_call([PYTHON, "-m", "build"])

# Create a new virtual environment
print("Creating a fresh virtual environment...")
subprocess.check_call([PYTHON, "-m", "venv", str(VENV)])
venv_python = VENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")

# Install the built wheel
wheels = list(DIST.glob("*.whl"))
if not wheels:
    print("No wheel file found in dist/ after build.", file=sys.stderr)
    sys.exit(1)
print(f"Installing {wheels[0].name} in test venv...")
subprocess.check_call([str(venv_python), "-m", "pip", "install", str(wheels[0])])

# Try importing gabm
print("Verifying import of gabm...")
subprocess.check_call([str(venv_python), "-c", "import gabm; print('gabm import OK')"])

# Optionally, check CLI entry point
try:
    print("Checking 'python -m gabm --help'...")
    subprocess.check_call([str(venv_python), "-m", "gabm", "--help"])
except Exception as e:
    print("Warning: 'python -m gabm --help' failed:", e)
    print("(This may be expected if no CLI is implemented.)")

print("Build and test install succeeded.")

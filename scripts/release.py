#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to sync and rebase a feature/release branch onto main.
Usage:
    python3 scripts/release.py --version 0.2.0 --branch release/0.2.0
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import argparse
import subprocess
import sys

def run(cmd, check=True):
    """
    Run a shell command and print it.
    Args:
        cmd (list): Command and arguments to run, e.g. ["git", "checkout", "main"]
        check (bool): If True, raise CalledProcessError on non-zero exit code
    Returns:
        int: The return code of the command
    """
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, check=check)
    return result.returncode

def main():
    """
    Main function to tag and push a release branch and version.
    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="Tag and push a release branch and version.")
    parser.add_argument("--version", required=True, help="Release version, e.g. 0.1.1")
    parser.add_argument("--branch", required=True, help="Release branch, e.g. release/0.1.1")
    parser.add_argument("--remotes", nargs='+', default=["origin", "upstream"], help="Remotes to push tag to")
    args = parser.parse_args()

    # Checkout or create branch
    try:
        run(["git", "checkout", args.branch])
    except subprocess.CalledProcessError:
        run(["git", "checkout", "-b", args.branch])

    tag_name = f"v{args.version}"
    tag_message = f"Release v{args.version}"

    # Create tag
    run(["git", "tag", "-a", tag_name, "-m", tag_message])

    # Push tag to remotes
    for remote in args.remotes:
        run(["git", "push", remote, tag_name])

    print(f"Release {tag_name} tagged and pushed to: {', '.join(args.remotes)}.")
    print(f"If this branch is not yet merged to main, open a PR from {args.branch} to main on GitHub.")

if __name__ == "__main__":
    # Run the main function
    main()

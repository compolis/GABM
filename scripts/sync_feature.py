#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to sync and rebase a feature/release branch onto main.
Usage:
    python3 scripts/sync_feature.py --branch release/0.2.0
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import sys
import subprocess

def main():
    """
    Main function to sync and rebase a feature/release branch onto main.
    """
    import argparse
    parser = argparse.ArgumentParser(description='Sync and rebase a feature/release branch onto main.')
    parser.add_argument('--branch', required=True, help='Branch name to rebase onto main')
    parser.add_argument('--upstream', default='upstream', help='Upstream remote name (default: upstream)')
    parser.add_argument('--main', default='main', help='Main branch name (default: main)')
    args = parser.parse_args()

    cmds = [
        ["git", "fetch", args.upstream],
        ["git", "checkout", args.main],
        ["git", "pull", args.upstream, args.main],
        ["git", "checkout", args.branch],
        ["git", "rebase", args.main]
    ]

    for cmd in cmds:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(result.stderr)
            sys.exit(result.returncode)
        else:
            print(result.stdout)
    print(f"Branch {args.branch} rebased onto {args.main}.")

if __name__ == '__main__':
    main()

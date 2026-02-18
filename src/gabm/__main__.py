#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Entry point for running the GABM application.
To run: python3 -m gabm
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.3.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import os
import os
import sys
import logging
from pathlib import Path
import random
# Visualization
import matplotlib.pyplot as plt
# Local imports
from gabm.abm.environment import Environment
from gabm.abm.agents.agent import Agent
from gabm.abm.agents.group import Group

def main():
    logging.info("\n--- GABM ---\n")

    # Set random seed for reproducibility
    random.seed(42)

    # Flexible group sizes
    n_negative = 2
    n_positive = 2
    n_neutral = 6

    # Number of communication rounds
    n_iterations = 5

    # For plotting: record opinions at each round (including initial)
    opinions_over_time = []

    # Initialize the environment
    env = Environment()

    # Create negative agents
    negative = env.groups_active[0] = Group(0, "Negative")
    for agent_id in range(n_negative):
        env.agents_active[agent_id] = Agent(agent_id, environment=env, opinion=-1.0)
        negative.add_member(env.agents_active[agent_id])

    # Create positive agents
    positive = env.groups_active[1] = Group(1, "Positive")
    for agent_id in range(n_negative, n_negative + n_positive):
        env.agents_active[agent_id] = Agent(agent_id, environment=env, opinion=1.0)
        positive.add_member(env.agents_active[agent_id])

    # Create neutral agents
    neutral = env.groups_active[2] = Group(2, "Neutral")
    for agent_id in range(n_negative + n_positive, n_negative + n_positive + n_neutral):
        env.agents_active[agent_id] = Agent(agent_id, environment=env, opinion=0.0)
        neutral.add_member(env.agents_active[agent_id])

    # Log the initial state of the environment
    n_agents = len(env.agents_active)
    logging.info(f"Initialized environment with {n_agents} agents.")

    # Record initial opinions
    opinions_over_time.append([agent.opinion for agent in env.agents_active.values()])

    # Calculate the average opinion of all agents in the environment and log it.
    avg_opinion = sum(agent.opinion for agent in env.agents_active.values()) / n_agents
    logging.info(f"Average opinion of all agents: {avg_opinion:.2f}")

    # List groups and their members
    for group in env.groups_active.values():
        logging.info(f"\n{group}")
        for member in group.list_members():
            logging.info(f"  - {member}")

    for iteration in range(n_iterations):
        logging.info(f"\n--- Communication round {iteration+1} ---")    
        # Each agent in the negative group communicates with a random neutral agent
        for agent in negative.members:
            other_agent = random.choice(list(neutral.members))
            agent.communicate(other_agent.id)
        # Each agent in the positive group communicates with a random neutral agent
        for agent in positive.members:
            other_agent = random.choice(list(neutral.members))
            agent.communicate(other_agent.id)
        # Record opinions after this round
        opinions_over_time.append([agent.opinion for agent in env.agents_active.values()])
        # Log the average opinion of all agents in the environment after communication
        avg_opinion = sum(agent.opinion for agent in env.agents_active.values()) / n_agents
        logging.info(f"Average opinion of all agents after communication: {avg_opinion:.2f}")
    logging.info("\nAgent communication demo complete.")

    # --- Plotting ---
    plt.figure(figsize=(8, 5))
    plt.boxplot(opinions_over_time, positions=range(len(opinions_over_time)), patch_artist=True)
    plt.xlabel('Round')
    plt.ylabel('Agent Opinion')
    plt.title('Distribution of Agent Opinions Over Time')
    plt.xticks(range(len(opinions_over_time)), [f"{i}" for i in range(len(opinions_over_time))])
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    # Save plot to file
    output_dir = Path("data/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_dir / "test.png")
    logging.info(f"Boxplot of agent opinions saved to {output_dir / 'test.png'}")

if __name__ == "__main__":
    # Set up logging to file and console
    log_dir = Path("data/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "run_main.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, mode="w"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    main()

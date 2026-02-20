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
from gabm.abm.environment import Environment, OpinionatedEnvironment, Nation
from gabm.abm.agent import Agent, Person
from gabm.abm.group import Group, OpinionatedGroup
from gabm.abm.opinion import OpinionTopicID, OpinionValue, OpinionValues, OpinionTopic, Opinion
from gabm.abm.attribute import GenderID, Gender

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
    env = OpinionatedEnvironment()

    # Create a gender map
    # Define gender IDs
    gender_id_0 = GenderID(0)
    gender_id_1 = GenderID(1)
    gender_id_2 = GenderID(2)
    # Define genders
    gender_0 = Gender(gender_id_0, "female", "A female gender.")
    gender_1 = Gender(gender_id_1, "male", "A male gender.")
    gender_2 = Gender(gender_id_2, "non-binary", "A non-binary gender.")
    gender_map = {
        gender_id_0: gender_0,
        gender_id_1: gender_1,
        gender_id_2: gender_2
    }
    # Default gender
    gender = gender_0

    # Define opinion topics and values
    # Define opinion topic IDs
    negative_opinion_topic_id = OpinionTopicID(0)
    neutral_opinion_topic_id = OpinionTopicID(1)
    positive_opinion_topic_id = OpinionTopicID(2)
    # Define opinion topics
    negative_opinion_topic = OpinionTopic(negative_opinion_topic_id, "negative", "A negative opinion.")
    neutral_opinion_topic = OpinionTopic(neutral_opinion_topic_id, "neutral", "A neutral opinion.")
    positive_opinion_topic = OpinionTopic(positive_opinion_topic_id, "positive", "A positive opinion.")
    # Add topics to environment
    env.opinions = {
        negative_opinion_topic_id: negative_opinion_topic,
        neutral_opinion_topic_id: neutral_opinion_topic,
        positive_opinion_topic_id: positive_opinion_topic
    }
    # Define opinion values for each topic
    env.opinion_values = {
        negative_opinion_topic_id: {
            OpinionValue(negative_opinion_topic_id, -2, "Strongly negative"),
            OpinionValue(negative_opinion_topic_id, -1, "Negative"),
            OpinionValue(negative_opinion_topic_id, 0, "Neutral"),
            OpinionValue(negative_opinion_topic_id, 1, "Positive"),
            OpinionValue(negative_opinion_topic_id, 2, "Strongly positive")
        },
        neutral_opinion_topic_id: {
            OpinionValue(neutral_opinion_topic_id, -2, "Strongly negative"),
            OpinionValue(neutral_opinion_topic_id, -1, "Negative"),
            OpinionValue(neutral_opinion_topic_id, 0, "Neutral"),
            OpinionValue(neutral_opinion_topic_id, 1, "Positive"),
            OpinionValue(neutral_opinion_topic_id, 2, "Strongly positive")
        },
        positive_opinion_topic_id: {
            OpinionValue(positive_opinion_topic_id, -2, "Strongly negative"),
            OpinionValue(positive_opinion_topic_id, -1, "Negative"),
            OpinionValue(positive_opinion_topic_id, 0, "Neutral"),
            OpinionValue(positive_opinion_topic_id, 1, "Positive"),
            OpinionValue(positive_opinion_topic_id, 2, "Strongly positive")
        }
    }
    # Define opinion values for easy access
    env.opinion_value_map = {}
    for topic_id, values in env.opinion_values.items():
        for value in values:
            env.opinion_value_map[value.opinion_topic_id] = value
    
    # Create negative agents
    negative = env.groups_active[0] = Group(0, "Negative")
    negative_opinions = {
        negative_opinion_topic_id: Opinion(
            negative_opinion_topic_id,
            OpinionValues({negative_opinion_topic_id: OpinionValue(negative_opinion_topic_id, 2, "Strongly positive")}),
            2),
        neutral_opinion_topic_id: Opinion(
            neutral_opinion_topic_id,
            OpinionValues({neutral_opinion_topic_id: OpinionValue(neutral_opinion_topic_id, 0, "Neutral")}),
            0),
        positive_opinion_topic_id: Opinion(
            positive_opinion_topic_id,
            OpinionValues({positive_opinion_topic_id: OpinionValue(positive_opinion_topic_id, -2, "Strongly negative")}),
            -2)
    }
    for agent_id in range(n_negative):
        gender = gender_map.get(random.choice([0, 1, 2]))
        env.agents_active[agent_id] = Person(
            agent_id, environment=env, year_of_birth=2000, 
            gender_map=gender_map, gender=gender, 
            opinions=negative_opinions)
        negative.add_member(env.agents_active[agent_id])

    # Create positive agents
    positive = env.groups_active[1] = Group(1, "Positive")
    positive_opinions = {
        negative_opinion_topic_id: Opinion(
            negative_opinion_topic_id,
            OpinionValues({negative_opinion_topic_id: OpinionValue(negative_opinion_topic_id, -2, "Strongly negative")}),
            -2),
        neutral_opinion_topic_id: Opinion(
            neutral_opinion_topic_id,
            OpinionValues({neutral_opinion_topic_id: OpinionValue(neutral_opinion_topic_id, 0, "Neutral")}),
            0),
        positive_opinion_topic_id: Opinion(
            positive_opinion_topic_id,
            OpinionValues({positive_opinion_topic_id: OpinionValue(positive_opinion_topic_id, 2, "Strongly positive")}),
            2)
    }
    for agent_id in range(n_negative, n_negative + n_positive):
        env.agents_active[agent_id] = Person(
            agent_id, environment=env, year_of_birth=2000, 
            gender_map=gender_map, gender=gender, 
            opinions=positive_opinions)
        positive.add_member(env.agents_active[agent_id])

    # Create neutral agents
    neutral = env.groups_active[2] = Group(2, "Neutral")
    neutral_opinions = {
        negative_opinion_topic_id: Opinion(
            negative_opinion_topic_id,
            OpinionValues({negative_opinion_topic_id: OpinionValue(negative_opinion_topic_id, 0, "Neutral")}),
            0),
        neutral_opinion_topic_id: Opinion(
            neutral_opinion_topic_id,
            OpinionValues({neutral_opinion_topic_id: OpinionValue(neutral_opinion_topic_id, 2, "Strongly positive")}),
            2),
        positive_opinion_topic_id: Opinion(
            positive_opinion_topic_id,
            OpinionValues({positive_opinion_topic_id: OpinionValue(positive_opinion_topic_id, 0, "Neutral")}),
            0)
    }
    for agent_id in range(n_negative + n_positive, n_negative + n_positive + n_neutral):
        env.agents_active[agent_id] = Person(
            agent_id, environment=env, year_of_birth=2000, 
            gender_map=gender_map, gender=gender, 
            opinions=neutral_opinions)
        neutral.add_member(env.agents_active[agent_id])

    # Log the initial state of the environment
    n_agents = len(env.agents_active)
    logging.info(f"Initialized environment with {n_agents} agents.")

    # Record initial opinions
    opinions_over_time.append(
        [agent.opinions.copy() for agent in env.agents_active.values()]
    )

    # Calculate the average opinions of all agents in the environment and log it.
    topic_name_to_id = {
        "negative": negative_opinion_topic_id,
        "neutral": neutral_opinion_topic_id,
        "positive": positive_opinion_topic_id
    }
    for topic_name, topic_id in topic_name_to_id.items():
        avg_opinion = sum(
            agent.opinions[topic_id].value if topic_id in agent.opinions else 0
            for agent in env.agents_active.values()
        ) / n_agents
        logging.info(f"Average opinion on '{topic_name}' of all agents: {avg_opinion:.2f}")

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
        opinions_over_time.append([agent.opinions.copy() for agent in env.agents_active.values()])
        # Log the average opinion of all agents in the environment after communication
        avg_opinions = {}
        for topic_name, topic_id in topic_name_to_id.items():
            avg_opinion = sum(
                agent.opinions[topic_id].value if topic_id in agent.opinions else 0
                for agent in env.agents_active.values()
            ) / n_agents
            avg_opinions[topic_name] = avg_opinion
            logging.info(f"Average opinion on '{topic_name}' of all agents after communication: {avg_opinion:.2f}")
    logging.info("\nAgent communication demo complete.")

    # --- Plotting ---
    output_dir = Path("data/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    colors = {"negative": "lightcoral", "neutral": "lightblue", "positive": "lightgreen"}
    for topic_name, topic_id in topic_name_to_id.items():
        plt.figure(figsize=(8, 5))
        topic_opinions = [
            [agent[topic_id].value if topic_id in agent else 0 for agent in opinions]
            for opinions in opinions_over_time
        ]
        plt.boxplot(topic_opinions, positions=range(len(opinions_over_time)), patch_artist=True, boxprops=dict(facecolor=colors[topic_name]), medianprops=dict(color='red'))
        plt.xlabel('Round')
        plt.ylabel(f"Opinions ({topic_name})")
        plt.title(f"Distribution of '{topic_name.capitalize()}' Opinions Over Time")
        plt.xticks(range(len(opinions_over_time)), [f"{i}" for i in range(len(opinions_over_time))])
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        filename = output_dir / f"opinions_{topic_name}.png"
        plt.savefig(filename)
        plt.close()
        logging.info(f"Boxplot of '{topic_name}' opinions saved to {filename}")

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

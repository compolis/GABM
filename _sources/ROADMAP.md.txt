# Roadmap


## Table of Contents
1. [Overview](#overview)
2. [1.0](#10)
3. [0.3](#03)


## Overview
This file outlines planned next steps and future goals.


## 1.0
- Criteria and features to be determined...


## 0.3
- Implement tidy-up scripts for logs and caches to help users and developers manage storage and maintain a clean environment.
- Add agent-based model (ABM) code
  - Agents
    - These will:
      - Belong to "networks" of other Agents
      - Be able to use LLM API prompts and responses to have "conversations" with other agents.
      - Have functions that modify them based on their state and the "influence" of a "conversation" with other agents.
  - Model
    - Agents organised to chat with other agents.
    - Graph output to reveal aggregate changes over time.
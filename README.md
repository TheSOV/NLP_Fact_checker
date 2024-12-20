# CrewAI NLP Project

A structured project for building AI agent crews using the CrewAI framework, focused on Natural Language Processing tasks.

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Components](#project-components)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project implements a CrewAI-based system for handling NLP tasks using multiple AI agents working together. The system is designed to be modular and extensible.

## Project Structure

```
NLP/
├── .env                # Environment variables (OPENAI_API_KEY, OPENAI_MODEL_NAME)
├── requirements.txt    # Project dependencies
├── main.py            # Main entry point
├── agents/            # Agent definitions
│   ├── base_agent.py
│   ├── researcher_agent.py
│   └── ...            # Additional specialized agents
├── corpus/            # Text data and corpus storage
│   └── ...            # Data files and documents
├── crews/             # Crew configurations
│   └── research_crew.py
├── tasks/             # Task definitions
│   ├── base_task.py
│   └── ...            # Specialized NLP tasks
└── tools/             # Custom tools and utilities
    └── base_tools.py
```

### Directory Descriptions

- **agents/**: Contains AI agent implementations for different NLP tasks
- **corpus/**: Stores text data, documents, and training materials
- **crews/**: Defines agent collaboration patterns and task coordination
- **tasks/**: Implements specific NLP task definitions and workflows
- **tools/**: Houses utility functions and helper tools for agents

## Prerequisites

- Python 3.10 or higher, less than 3.13
- C++ 14 Build Tools and Compiler
  - Note: If C++ is installed after Python, Python needs to be reinstalled
- pip (Python package manager)

## Installation
# Install C++ 14 first and then, python

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd NLP
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Configure the following API keys in `.env`:
   - OPENAI_API_KEY
   - OPENAI_MODEL_NAME


## Usage

Run the main application:
```bash
python main.py
```

## Project Components

### Agents
Located in `agents/`, our specialized AI agents include:

- **Input Analyzer Agent**: Analyzes and processes input text to determine the nature of queries and required tasks
- **Searcher Agent**: Performs information retrieval and search operations
- **QA Agent**: Handles question-answering tasks using the processed information
- **Fact Verifier Agent**: Validates facts and claims against reliable sources

### Tasks
Located in `tasks/`, our NLP tasks include:

- **Input Analysis Task**: Initial processing and classification of input text
- **Search Task**: Information retrieval from specified sources
- **QA Review Task**: Question answering and response generation
- **Fact Verification Task**: Fact-checking and validation procedures

### Crews
Located in `crews/`, our agent teams include:

- **Fact Checker Crew**: Coordinates multiple agents for comprehensive fact verification
  - Combines Input Analysis, Search, and Fact Verification capabilities
  - Orchestrates the workflow between different agents
  - Ensures thorough validation of information

### Tools
Located in `tools/`, containing utility functions and shared resources used by agents for:
- Text processing
- Data validation
- Agent communication
- Resource management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT

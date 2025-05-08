# AI Fact-Checking Application
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/TheSOV/NLP_Fact_checker)

Detailed information at [[DeepWiki](https://deepwiki.com/TheSOV/NLP_Fact_checker)

## 📋 Table of Contents

### 🚀 Project Overview
- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Project Components Detailed](#project-components-detailed)

### 🛠 Technical Architecture
- [Embedding and Search](#technical-architecture)
- [Confidence Scoring](#confidence-scoring)
- [Multilingual Support](#multilingual-support)

### 📦 Corpus Management
- [Understanding the Corpus](#corpus-management)
- [Creating Your Own Corpus](#creating-your-own-corpus)
- [Corpus Creation Steps](#3-corpus-creation-steps)

### 🔧 Environment Setup
- [Environment Configuration](#environment-configuration)
- [Prerequisites](#prerequisites)
- [Installation](#installation)

### 💻 Usage and Examples
- [Running the Application](#running-the-application)
- [Example Usage](#example-usage)

### 📜 Additional Information
- [License](#license)
- [References](#references)

### 🤝 Contributing
- [How to Contribute](#contributing)

---

## 🌟 Key Features

A multilingual fact-checking system powered by CrewAI, designed to verify statements using NLP techniques.

### Features Highlights
- **Multilingual Support**: Fact-check and translate content across multiple languages
- **Semantic Search**: Embedding-based search for relevant information
- **Confidence Scoring**: Confidence calculation for fact verification
- **Flexible Fact-Checking**: Supports both Wikipedia and internet-based fact-checking

## Project Structure

```
NLP_Fact_checker/
├── agents/           # AI agent definitions
│   ├── fact_verifier_agent.py       # Handles core logic for fact validation
│   ├── input_analyser_agent.py      # Processes and interprets input queries
│   ├── internet_searcher_agent.py   # Performs web-based information retrieval
│   ├── meta_searcher_agent.py       # Searches the articles contents based on the article name
│   ├── searcher_agent.py            # General-purpose information search
│   ├── summarizer_agent.py          # Generates concise content summaries
│   └── translator_agent.py          # Handles multilingual translation
│
├── corpus/           # Embeddings and document storage
│   ├── embeddings/   # Pre-computed vector embeddings
│   └── documents/    # Source documents and reference materials
│
├── crews/            # Agent collaboration configurations
│   ├── fact_checker_crew.py         # Coordinates Wikipedia-based fact verification
│   ├── generic_translation_crew.py  # Handles generic text translation
│   ├── input_analyzer_crew.py       # Processes and analyzes input queries
│   ├── internet_fact_checker_crew.py # Coordinates internet-based fact-checking
│   ├── meta_search_crew.py          # Manages metadata and source searching
│   └── translation_crew.py          # Handles translations with structured output
│
├── flows/            # Workflow management
│   ├── fact_checker_flow.py         # Wikipedia-based fact-checking workflow
│   ├── internet_fact_checker_flow.py # Internet-based fact-checking workflow
│   └── get_summarized_source_flow.py # Source content summarization
│
├── tasks/            # Specific task implementations
│   ├── fact_verification_task.py    # Core fact-checking task
│   ├── input_analysis_task.py       # Input query processing
│   ├── internet_search_task.py      # Web-based information retrieval
│   ├── metadata_search_task.py      # Metadata and source information search
│   ├── search_task.py               # General search functionality
│   ├── summarize_task.py            # Content summarization
│   └── translation_task.py          # Language translation implementation
│
├── tools/            # Search and utility tools
│   ├── search_manager.py            # Singleton vector store management
│   └── search_tools.py              # RAG and metadata search capabilities
│
├── utils/            # Utility modules
│   └── embeddings.py                # Singleton embeddings management
│
├── web/              # Web interface components
│   ├── components/   # Reusable UI components
│   ├── static/       # Static assets (CSS, images)
│   └── templates/    # HTML templates
│
├── .env             # Environment configuration
├── requirements.txt # Project dependencies
└── main.py          # Application entry point
```

### Project Structure Breakdown

#### 🏗️ Directory Purpose and Design

- **`agents/`**: Contains specialized AI agents responsible for specific tasks
  - Each agent is designed with a single responsibility principle
  - Modular design allows easy extension and modification

- **`corpus/`**: Stores knowledge base and computational resources
  - `embeddings/`: Pre-computed vector representations for fast semantic search
  - `documents/`: Reference materials and source documents

- **`crews/`**: Defines collaborative workflows for complex tasks
  - Orchestrates multiple agents to achieve comprehensive goals
  - Implements different fact-checking and translation strategies

- **`flows/`**: Manages end-to-end workflows
  - Defines the sequence of operations for different fact-checking scenarios
  - Handles state management and inter-agent communication
  - Enables the integration of AI-driven and traditional programming approaches

- **`tasks/`**: Granular task implementations
  - Breaks down complex operations into manageable, focused tasks
  - Supports modular and reusable task design

- **`tools/`**: Provides utility functions and search capabilities
  - Implements singleton patterns for resource management
  - Offers advanced search and embedding techniques

- **`utils/`**: Contains core utility modules
  - Provides singleton embedding management
  - Ensures consistent resource initialization

- **`web/`**: Web interface components
  - Supports potential web-based frontend
  - Separates UI concerns from core logic

## Project Components Detailed

### 🤖 Agents (`/agents`)
Our specialized AI agents handle different aspects of fact-checking:
- `fact_verifier_agent.py`: Validates and cross-references facts
- `input_analyser_agent.py`: Processes and interprets input queries
- `internet_searcher_agent.py`: Performs web-based information retrieval
- `meta_searcher_agent.py`: Searches metadata and source information
- `searcher_agent.py`: General-purpose information search
- `summarizer_agent.py`: Generates concise summaries
- `translator_agent.py`: Handles language translation

### 🚢 Crews (`/crews`)
Collaborative agent teams that coordinate complex tasks:
- `fact_checker_crew.py`: Manages fact verification workflow
- `generic_translation_crew.py`: Handles generic text translation
- `input_analyzer_crew.py`: Processes and analyzes input queries
- `internet_fact_checker_crew.py`: Coordinates internet-based fact-checking
- `meta_search_crew.py`: Manages metadata and source searching
- `translation_crew.py`: Specialized translation coordination

### 📋 Tasks (`/tasks`)
Specific task implementations for different workflow stages:
- `fact_verification_task.py`: Core fact-checking logic
- `input_analysis_task.py`: Input query processing
- `internet_search_task.py`: Web-based information retrieval
- `metadata_search_task.py`: Metadata and source information search
- `search_task.py`: General search functionality
- `summarize_task.py`: Content summarization
- `translation_task.py`: Language translation implementation

### 🔧 Tools (`/tools`)
Utility functions and search management:
- `search_manager.py`: Manages vector store and embedding resources
- `search_tools.py`: Provides RAG and metadata search capabilities

### 🔀 Flows (`/flows`)
Workflow management for different fact-checking scenarios:
- `fact_checker_flow.py`: Wikipedia-based fact-checking workflow
- `get_summarized_source_flow.py`: Source content summarization
- `internet_fact_checker_flow.py`: Internet-based fact-checking workflow

## Corpus Management

### Understanding the Corpus

The `corpus/` directory is a critical component of the fact-checking system, responsible for managing knowledge sources and embeddings:

```
corpus/
├── zipped/           # Original compressed source files
├── unzipped/         # Extracted source documents
├── embeddings/       # Generated vector embeddings
├── create_embeddings.py  # Script to process and vectorize documents
└── unzip_files.py    # Utility to extract compressed files
```

### Creating Your Own Corpus

#### Preparing Your Corpus

The corpus is a critical component of the fact-checking system and is responsible for providing knowledge sources and embeddings. To create your own corpus, follow these steps:

##### 1. Gather Source Documents

The corpus currently supports Wikipedia XML dumps as source documents. You can download the XML dumps from the following sources:

- [Wikipedia XML Dumps](https://dumps.wikimedia.org/)
- [Recommended Mirror](https://mirror.accum.se/mirror/wikimedia.org/dumps/enwiki/20241001/)

##### 2. Document Requirements

The corpus must meet the following requirements:

- The corpus must be a Wikipedia XML dump (files that contains article text, like this one [enwiki-20241001-pages-articles1.xml-p1p41242.bz2](https://mirror.accum.se/mirror/wikimedia.org/dumps/enwiki/20241001/enwiki-20241001-pages-articles1.xml-p1p41242.bz2))
- Currently, only English language sources are supported to be used as corpus

#### 3. Corpus Creation Steps

##### Automatic Corpus Generation
```bash
# Place bz2 files containing the XML in corpus/zipped/. It accepts any number of files.
python corpus/unzip_files.py     # Extract compressed files
python corpus/create_embeddings.py  # Generate embeddings
```

#### Embedding Generation Process
1. Extract text from source documents
2. Clean and normalize text
3. Split into manageable chunks
4. Generate vector embeddings
5. Store in FAISS vector database

## Environment Configuration

### `.env` File Setup

The `.env` file contains essential configuration for the application:

```bash
# OpenAI API Configuration
OPENAI_API_KEY="your_openai_api_key"  # Required for AI-powered fact-checking
OPENAI_MODEL_NAME="gpt-4o-mini"       # Specify the OpenAI model to use

# Serper API Configuration (for web searches)
SERPER_API_KEY="your_serper_api_key"                     # Optional: API key for web search functionality
```

### Configuration Details

1. **OpenAI API Key**:
   - Mandatory for using AI-powered fact-checking
   - Obtain from [OpenAI Platform](https://platform.openai.com/account/api-keys)
   - Ensure the key has appropriate permissions for text generation and analysis

2. **OpenAI Model Selection**:
   - Currently using `gpt-4o-mini`
   - Provides a balance of performance and cost-effectiveness
   - Can be changed to other compatible OpenAI models as needed

3. **Serper API Key**:
   - Used for web-based searches
   - Can be obtained from [Serper.dev](https://serper.dev/) if web search is required


## Technical Architecture

### Embedding and Search
- Uses `all-MiniLM-L6-v2` multilingual embedding model
- FAISS vector store for efficient semantic search

### Confidence Scoring
- Calculates semantic similarity between query and retrieved fragments
- Uses cosine similarity to measure relevance
- Confidence is the maximum similarity score between query and fragments
- Ranges from 0.0 (no match) to 1.0 (perfect match)
- Provides a simple, interpretable confidence metric

### Multilingual Support
- Automatic language detection
- Translation of queries and results
- Supports fact-checking in multiple languages

## Quick Start

### Prerequisites
- On Windows the project requires Microsoft Visual C++ 14.0, from the C++ Build Tools. If the compiler is installed after Python, it is required to reinstall Python.
- Python version 3.10 (recommended) or later, but before version 3.12

### Installation
```bash
git clone https://github.com/TheSOV/NLP_Fact_checker.git
cd NLP_Fact_checker
pip install -r requirements.txt
```

### Running the Application
```bash
python main.py
```

## License
[MIT]

## References
- [CrewAI Documentation](https://github.com/joaomdmoura/CrewAI)
- [HuggingFace Embeddings](https://huggingface.co/models)
- [FAISS Vector Search](https://github.com/facebookresearch/faiss)

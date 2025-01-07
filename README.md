# AI Fact-Checking Application

A multilingual fact-checking system powered by CrewAI, designed to verify statements using NLP techniques.

## Key Features

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

## Technical Details

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

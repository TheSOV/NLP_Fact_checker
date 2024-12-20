from crewai import Task
from agents.json_extractor_agent import json_extractor
from pydantic import BaseModel
from typing import Dict, List, Optional

class SourcesOutput(BaseModel):
    """Output schema for sources extraction."""
    wikipedia_articles: List[str]
    other_sources: Dict[str, str]

# Create JSON extraction task
json_extraction_task = Task(
    description="""Extract Wikipedia article titles and other sources from the content:
    1. Find all Wikipedia article titles mentioned in the content
    2. Collect other sources of interest with their URLs
    3. Format the output according to the specified structure
    
    Content to Process: {fact_verifier_response}
    
    Rules for extraction:
    1. Wikipedia articles should be a simple list of titles in English
    2. Other sources should be key-value pairs where:
       - Key: The title or name of the source
       - Value: The URL of the source
    3. Only include other sources that have URLs
    4. Remove any duplicates
    """,
    agent=json_extractor,
    expected_output="""A JSON object containing two main sections:
    1. 'wikipedia_articles': A list of Wikipedia article titles
    2. 'other_sources': A dictionary of source titles and their URLs""",
    output_json=SourcesOutput
)

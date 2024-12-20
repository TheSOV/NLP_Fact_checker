from crewai import Task
from agents.summarizer_agent import summarizer
from pydantic import BaseModel
from typing import List, Optional

# Create summarize task
summarize_task = Task(
    description="""Create a comprehensive and well-structured summary from the provided search results:
    1. Analyze the provided search fragments
    2. Identify and remove redundant information
    3. Organize the information in a logical flow
    4. Create a coherent article that presents the information clearly
    5. Maintain factual accuracy while improving readability""",
    agent=summarizer,
    expected_output="""A well-structured article that synthesizes the search results into a coherent narrative,
    with redundant information eliminated and maintaining factual accuracy.
    The article should have a clear flow and be easy to read while preserving all important information."""
)

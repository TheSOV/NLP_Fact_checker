from crewai import Task
from agents.meta_searcher_agent import meta_searcher
from pydantic import BaseModel
from typing import List, Optional
from tools.meta_search_tools import MetadataSearchTool

meta_search_tool = MetadataSearchTool(result_as_answer=True)

# Create search task
meta_search_task = Task(
    description="""Search through the literature, using the metadata search tool, and searching by the Wikipedia article title mentioned in the source, all the fragments that conform the articles, and return the fragments in an article format, eliminating the textually repeated fragments. Get the Wikipedia article title from the following text on the section 'Sources (Wikipedia articles)'. The text might be in different languages, always make the search in English: "Text where the Wikipedia article title is mentioned: "{article_title}" """,
    agent=meta_searcher,
    expected_output="""The found fragments.""",
    tools=[meta_search_tool]
)

from crewai import Crew
from agents.meta_searcher_agent import meta_searcher
from agents.summarizer_agent import summarizer
from agents.translator_agent import translator
from tasks.metadata_search_task import meta_search_task
from tasks.summarize_task import summarize_task

# Create meta search crew
meta_search_crew = Crew(
    agents=[meta_searcher, summarizer],
    tasks=[meta_search_task, summarize_task],
    verbose=True  # To get detailed output of the crew's work
)

from crewai import Crew
from agents.meta_searcher_agent import meta_searcher
from agents.summarizer_agent import summarizer
from agents.translator_agent import translator
from tasks.metadata_search_task import meta_search_task
from tasks.summarize_task import summarize_task
from tasks.translation_task import translation_task_chain

# Create meta search crew
meta_search_crew = Crew(
    agents=[meta_searcher, summarizer, translator],
    tasks=[meta_search_task, summarize_task, translation_task_chain],
    verbose=True  # To get detailed output of the crew's work
)

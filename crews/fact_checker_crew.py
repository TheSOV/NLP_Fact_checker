from crewai import Crew
from agents.searcher_agent import searcher
from agents.fact_verifier_agent import verifier_agent
from tasks.search_task import search_task
from tasks.fact_verification_task import verification_task

# Create fact checker crew
fact_checker_crew = Crew(
    agents=[searcher, verifier_agent],
    tasks=[search_task, verification_task],
    verbose=True,  # To get detailed output of the crew's work
)


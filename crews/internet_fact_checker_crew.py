from crewai import Crew
from agents.internet_searcher_agent import internet_searcher
from agents.fact_verifier_agent import verifier_agent
from tasks.internet_search_task  import internet_search_task
from tasks.fact_verification_task import verification_task

# Create fact checker crew
internet_fact_checker_crew = Crew(
    agents=[internet_searcher, verifier_agent],
    tasks=[internet_search_task, verification_task],
    verbose=True,  # To get detailed output of the crew's work
    planning=True,
)


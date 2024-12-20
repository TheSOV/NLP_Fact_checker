from crewai import Crew
from agents.input_analyser_agent import input_analyzer_agent
from agents.searcher_agent import searcher
from agents.fact_verifier_agent import verifier_agent
from agents.qa_agent import qa_agent
from tasks.input_analysis_task import input_analysis_task
from tasks.search_task import search_task
from tasks.fact_verification_task import verification_task
from tasks.qa_task import qa_task

# Create fact checker crew
fact_checker_crew = Crew(
    agents=[input_analyzer_agent, searcher, verifier_agent],
    tasks=[input_analysis_task, search_task, verification_task],
    verbose=True,  # To get detailed output of the crew's work
    planning=True,
)

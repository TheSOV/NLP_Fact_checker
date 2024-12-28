from crewai import Crew
from agents.input_analyser_agent import input_analyzer_agent
from tasks.input_analysis_task import input_analysis_task


# Create fact checker crew
input_analyzer_crew = Crew(
    agents=[input_analyzer_agent],
    tasks=[input_analysis_task],
    verbose=True,  # To get detailed output of the crew's work
    planning=False,
)


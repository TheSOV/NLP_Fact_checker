from crewai import Crew
from agents.translator_agent import translator
from tasks.translation_task import translation_task_pure

# Create generic translation crew
generic_translation_crew = Crew(
    agents=[translator],
    tasks=[translation_task_pure],
    verbose=True,  # To get detailed output of the crew's work
    planning=False,  # No need for planning in a single-task crew
)

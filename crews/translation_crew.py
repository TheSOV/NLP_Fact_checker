from crewai import Crew
from agents.translator_agent import translator
from tasks.translation_task import translate_fact_verification_task

# Create generic translation crew
translation_crew = Crew(
    agents=[translator],
    tasks=[translate_fact_verification_task],
    verbose=True,  # To get detailed output of the crew's work
)

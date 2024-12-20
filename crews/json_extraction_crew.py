from crewai import Crew
from agents.json_extractor_agent import json_extractor
from tasks.json_extraction_task import json_extraction_task

# Create JSON extraction crew
json_extraction_crew = Crew(
    agents=[json_extractor],
    tasks=[json_extraction_task],
    verbose=True  # To get detailed output of the crew's work
)

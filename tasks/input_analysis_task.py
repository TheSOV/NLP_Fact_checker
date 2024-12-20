from crewai import Task
from agents.input_analyser_agent import input_analyzer_agent
from pydantic import BaseModel
from typing import List
import time

class InputAnalysisOutput(BaseModel):
    """Output schema for input analysis."""
    original_request: str
    request_in_english: str
    verification_facts: List[str]
    possible_questions: List[str]
    original_language: str

# Create input analysis task
input_analysis_task = Task(
    description="""Your task is to analyze the user input and break it down into structured components.
    
    Your analysis must include:
    1. The original request exactly as provided, in the original language.
    2. The request in English.
    3. The facts that need verification. These facts will result from the decomposition of the original request into verification facts. Do not generate new facts or asumptions from the original request, only decompose it. Each fact must contain all the information necessary to make a search for verification by itself, as is no other fact could be accessed to understand it.
    4. The possible questions that would be useful to be answered to verify the claims.
    5. The detected language of the original text. If more than one language is detected, choose the one with the highest prevalence.
    
    The user input to analyze is the following: '''{user_input}'''""",
    agent=input_analyzer_agent,
    expected_output="""A JSON with the following fields: "original_request", "request_in_english", "verification_facts", "possible_questions", and "original_language.""",
    output_json=InputAnalysisOutput,
)

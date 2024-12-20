from crewai import Task
from agents.translator_agent import translator
from pydantic import BaseModel
from typing import List, Optional

# Create translation task
class TranlationFactVerificationOutput(BaseModel):
    """Output schema for fact verification analysis."""
    fragments: List[str]
    explanation: str
    classification: str

translate_fact_verrification_task = Task(
    description="""From the received input, translate the "fragments", the "explanation" and the "classification", to the target language if the source language is different. To do this, you must:
    1. Understand the context and meaning of the source content
    2. Identify any specialized terminology or domain-specific language
    3. Translate while preserving the original meaning and context
    4. Ensure cultural appropriateness and localization
    5. Maintain the original formatting and structure

    In case the source language is the same as the target language, make no translation, and return the original content.
    
    Target Language: {target_language}
    Content to Translate: {fact_verifier_response}
    """,
    agent=translator,
    expected_output="""A JSON object containing three main sections:
    1. 'fragments': A list of translated fragments if the source language is different, else the original fragments
    2. 'explanation': A translated explanation, if the source language is different, else the original explanation
    3. 'classification': A translated classification, if the source language is different, else the original classification""",
    output_json=TranlationFactVerificationOutput
)

translation_task_pure = Task(
    description="""Translate the provided content into the specified target language:
    1. Understand the context and meaning of the source content
    2. Identify any specialized terminology or domain-specific language
    3. Translate while preserving the original meaning and context
    4. Ensure cultural appropriateness and localization
    5. Maintain the original formatting and structure
    
    Target Language: {target_language}
    Content to Translate: {content}
    """,
    agent=translator,
    expected_output="""A high-quality translation of the provided content in the target language,
    maintaining the original meaning, context, and formatting."""
)

translation_task_chain = Task(
    description="""Translate the provided content into the specified target language:
    1. Understand the context and meaning of the source content
    2. Identify any specialized terminology or domain-specific language
    3. Translate while preserving the original meaning and context
    4. Ensure cultural appropriateness and localization
    5. Maintain the original formatting and structure
    
    Target Language: {target_language}
    """,
    agent=translator,
    expected_output="""A high-quality translation of the provided content in the target language,
    maintaining the original meaning, context, and formatting."""
)
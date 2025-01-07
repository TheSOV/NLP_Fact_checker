from crewai import Task
from agents.fact_verifier_agent import verifier_agent
from agents.searcher_agent import searcher
from agents.input_analyser_agent import input_analyzer_agent
from typing import List, Optional
from pydantic import BaseModel
import time

from tasks.input_analysis_task import input_analysis_task
from tasks.search_task import search_task

class FactVerificationOutput(BaseModel):
    """Output schema for fact verification analysis."""
    sources: List[str]
    fragments: List[str]
    explanation: str
    classification: str

verification_task = Task(
    description="""Using the search results and input analysis, determine the request_in_english and all the verification_facts were verified, refused, or if there's NOT ENOUGH INFORMATION.

    You will catalog as TRUE, when there is enough evidence to support the request_in_english and all the verification_facts.
    You will catalog as FALSE, when there is enough evidence to refute the request_in_english and all the verification_facts.
    You will catalog as NOT ENOUGH INFORMATION, when there is not enough evidence to support or refute the request_in_english and all the verification_facts. If any of the parts of the request_in_english and all the verification_facts are missing from the search results, you will catalog as NOT ENOUGH INFORMATION. If it is necessary to makes an assumption, you will catalog as NOT ENOUGH INFORMATION.
    
    Your task is to:
    1. Review the search results, the original request and the verification_facts. Pay special attention to all the elemnts of the request_in_english, to ensure if information exists about them.
    2. Evaluate the evidence for and against the request_in_english and all the verification_facts generated from it. Check all the elements of the request_in_english, to ensure if information exists about them.
    3. Make a determination based SOLELY on the provided information. Never use your own knowledge or assumptions.
    4. Provide a clear explanation for your veredict

    Always think, explain and write to yourself the support or refute of the request_in_english and all the verification_facts and then give the answer before giving it to the user. All answers in English. You cannot use tools.
    
    The user input to analyze is the following: '''{user_input}'''""",
    agent=verifier_agent,
    expected_output="""Provide a JSON file with the following fields:
    1. "sources" (Wikipedia articles or Internet Article): Provide all the Wikipedia articles or Internet Articles (the sources must be selected from the search results, from the "wikipedia_article_source" or the "internet_article_source" fields only, and must be textually cited, because will be used in future searches and must be accurate) from where you got useful information to support or refute the request_in_english and all the verification_facts. Each source must appear only once. Omit sources unrelated to the claims and facts to be verified.
    2. "fragments": Fragments of Sources (Wikipedia articles or Internet Article) from where you got useful information to support or refute the request_in_english and all the verification_facts. This field must be textually cited, and must not be empty unless there is not enough information to support or refute the claim. The fragments can be only included if the information in it is useful to support or refute the initial input and/or one or more claims. If possible, include at least one fragment for each Wikipedia article or Internet Article. Exclude fragments unrelated to the claims and fact verifications. Add to the end of each fragment, between parenthesis, the source.
    3. "explanation": based on the sources and fragments, provide a clear explanation for your verdict responding to all the aspects of the request_in_english. The explanation is for the user whoe made the initial request, so it will not understand terms like verification_facts or request_in_english, so just give the answer to the user in a natural way.
    4. "classification": A clear verdict (TRUE/FALSE/NOT ENOUGH INFORMATION) based on the if was possible to support or refute the all the parts of the claim. IMPORTANT: classification can be only TRUE if all the parts of the claim were verified, False if at least one part of the claim was refused and NOT ENOUGH INFORMATION if any of the parts of the claim is missing from the search results and cannot be supported or refuted.""",
    output_json=FactVerificationOutput
)
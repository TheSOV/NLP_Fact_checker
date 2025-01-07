# Flow for fact-checking using internet sources (beyond Wikipedia)
# This flow follows these steps:
# 1. Analyze input to detect language and translate to English if needed
# 2. Search internet sources and verify facts
# 3. Calculate confidence based on semantic similarity
# 4. Translate results back to original language if needed

from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from crewai.flow.flow import Flow, listen, start
from crews.input_analyzer_crew import input_analyzer_crew
from crews.internet_fact_checker_crew import internet_fact_checker_crew
from crews.translation_crew import translation_crew
from pydantic import BaseModel
from typing import Any
import json
from utils.embeddings import embeddings

class FactCheckerState(BaseModel):
    """State schema for internet fact checker flow.
    Tracks:
    - input_analyzer: Results from language detection and translation
    - fact_checker: Results from fact verification process
    - translation: Final results translated to user's language
    - search_results: Raw search results from internet sources
    - confidence_score: Semantic similarity score between query and evidence
    """
    input_analyzer: dict[str, Any] = {}
    fact_checker: dict[str, Any] = {}
    translation: dict[str, Any] = {}
    search_results: list[Any] = []
    confidence_score: float = 0

class InternetFactCheckerFlow(Flow):
    def __init__(self, user_input: str):
        """Initialize internet fact checker flow with user's query"""
        super().__init__()
        assert isinstance(user_input, str)
        
        self.inputs = {"user_input": user_input}
        self._state = FactCheckerState()

    @start()
    def analyze_input(self):
        """Step 1: Analyze input text for language detection
        Also translates non-English queries to English"""
        self._state.input_analyzer = input_analyzer_crew.kickoff(inputs=self.inputs).to_dict()

    @listen(analyze_input)
    def check_facts(self):
        """Step 2: Perform fact checking using internet sources
        - Searches internet for relevant articles and sources
        - Verifies claims against found sources
        - Extracts supporting evidence"""
        self._state.fact_checker = internet_fact_checker_crew.kickoff(inputs={
            "user_input": json.dumps(self._state.input_analyzer),
        }).to_dict()

        self._state.search_results = internet_fact_checker_crew.tasks[0].output.raw # RAG's results
        print("Internet search results:")
        print(self._state.search_results)
        
        # Calculate confidence score using semantic similarity
        query_english = self._state.input_analyzer["request_in_english"]
        query_embedding = embeddings.embed_query(query_english) 

        fragments = internet_fact_checker_crew.tasks[1].output.to_dict().get("fragments", None)
        
        # Handle case when no fragments are found
        if not fragments:
            self._state.confidence_score = 0.0
            return

        fragments_embeddings = embeddings.embed_documents(fragments) 
        
        similarities = cosine_similarity([query_embedding], fragments_embeddings)[0]

        self._state.confidence_score = max(similarities) 
        print("confidence: ", self._state.confidence_score)
        ##

    @listen(check_facts)
    def translate_facts(self):
        """Step 3: Translate results back to original language if needed
        Also verifies source URLs and marks them as internet sources"""
        if (self._state.input_analyzer["original_language"].lower() == "en" or 
            self._state.input_analyzer["original_language"].lower() == "english"):
            self._state.translation = self._state.fact_checker
        else:
            self._state.translation = translation_crew.kickoff(inputs={
                "fact_verifier_response": json.dumps(self._state.fact_checker),
                "target_language": self._state.input_analyzer["original_language"],
                }).to_dict()

        # Process sources and mark them as internet sources
        temp = {}
        for source in self._state.fact_checker["sources"]:
            try:
                temp[source] = {
                    "name": source,
                    "verified": True,
                    "internet": True
                }
            except Exception as e:
                print(f"Error processing source '{source}': {str(e)}")
                temp[source] = {
                    "name": source,
                    "verified": True,
                    "internet": True
                }

        self._state.translation["sources"] = temp
        self._state.fact_checker["sources"] = temp
        
        return self._state
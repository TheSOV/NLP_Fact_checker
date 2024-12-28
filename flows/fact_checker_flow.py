from crewai.flow.flow import Flow, listen, start
from crews.input_analyzer_crew import input_analyzer_crew
from crews.fact_checker_crew import fact_checker_crew
from crews.translation_crew import translation_crew
from pydantic import BaseModel
from typing import Any
import json

from tasks.metadata_search_task import meta_search_tool

class FactCheckerState(BaseModel):
    input_analyzer: dict[str, Any] = {}
    fact_checker: dict[str, Any] = {}
    translation: dict[str, Any] = {}

class FactCheckerFlow(Flow):
    def __init__(self, user_input: str):
        super().__init__()
        assert isinstance(user_input, str)
        
        self.inputs = {"user_input": user_input}
        self._state = FactCheckerState()

    @start()
    def analyze_input(self):
        self._state.input_analyzer = input_analyzer_crew.kickoff(inputs=self.inputs).to_dict()

    @listen(analyze_input)
    def check_facts(self):
        self._state.fact_checker = fact_checker_crew.kickoff(inputs={
            "user_input": json.dumps(self._state.input_analyzer),
        }).to_dict()

    @listen(check_facts)
    def translate_facts(self):
        if (self._state.input_analyzer["original_language"].lower() == "en" or 
            self._state.input_analyzer["original_language"].lower() == "english"):
            self._state.translation = self._state.fact_checker
        else:
            self._state.translation = translation_crew.kickoff(inputs={
                "fact_verifier_response": json.dumps(self._state.fact_checker),
                "target_language": self._state.input_analyzer["original_language"],
                }).to_dict()

        temp = {}

        for source in self._state.fact_checker["sources"]:
            temp[source] = meta_search_tool.verify_title(source)

        self._state.translation["sources"] = temp
        self._state.fact_checker["sources"] = temp
        
        return self._state
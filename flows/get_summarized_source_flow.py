from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

from crews.meta_search_crew import meta_search_crew
from crews.generic_translation_crew import generic_translation_crew

class SummarizedSourceFlowState(BaseModel):
    source: str = ""
    target_language: str = ""
    summary: str = ""    
    translated_summary: list = ""
    

class GetSummarizedSourceFlow(Flow):
    def __init__(self, source: str, target_language: str):
        super().__init__()
        assert isinstance(source, str)
        self._state = SummarizedSourceFlowState()

        self._state.source = source
        self._state.target_language = target_language

    @start()
    def get_summarized_source(self):
        self._state.summary = meta_search_crew.kickoff(inputs={
            "article_title": self._state.source
        }).raw

    
    @listen(get_summarized_source)
    def translate_summary(self):
        if self._state.target_language.lower() == "en" or self._state.target_language.lower() == "english":
            self._state.translated_summary = self._state.summary
        else:
            self._state.translated_summary = generic_translation_crew.kickoff(inputs={
                "content": self._state.summary,
                "target_language": self._state.target_language
            }).raw

        return self._state

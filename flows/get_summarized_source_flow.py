# Flow for retrieving and summarizing source content
# This flow handles:
# 1. Retrieving source content (from Wikipedia)
# 2. Summarizing the content
# 3. Translating the summary to the requested language

from crewai import task
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

from crews.meta_search_crew import meta_search_crew
from crews.generic_translation_crew import generic_translation_crew

class SummarizedSourceFlowState(BaseModel):
    """State schema for source summarization flow.
    Tracks:
    - source: The source being processed
    - target_language: Desired language for the summary
    - summary: Summarized content
    - translated_summary: Final translated summary
    """
    source: str = ""
    target_language: str = ""
    summary: str = ""    
    translated_summary: str = ""

class GetSummarizedSourceFlow(Flow):
    def __init__(self, source: str, target_language: str):
        """Initialize source summarization flow
        Args:
            source: title of the source to summarize
            target_language: Language code for the desired summary translation
        """
        super().__init__()
        assert isinstance(source, str)
        assert isinstance(target_language, str)
        
        self._state = SummarizedSourceFlowState()
        self._state.source = source
        self._state.target_language = target_language

    @start()
    def get_summarized_source(self):
        """Step 1: Retrieve and summarize the source content
        - Retrieves the full content from the source
        - Creates a concise summary highlighting key points
        - Maintains important context and facts"""
        self._state.summary = meta_search_crew.kickoff(inputs={
            "article_title": self._state.source
        }).raw

        print(meta_search_crew.tasks[0].output.raw)

    @listen(get_summarized_source)
    def translate_summary(self):
        """Step 2: Translate the summary to target language
        - Translates the summary while preserving meaning
        - Handles special terms and context appropriately
        - Returns error message if translation fails"""
        if self._state.target_language.lower() == "en" or self._state.target_language.lower() == "english":
            # If target is English, no translation needed
            self._state.translated_summary = self._state.summary
        else:
            # Translate summary to target language
            self._state.translated_summary = generic_translation_crew.kickoff(inputs={
                "content": self._state.summary,
                "target_language": self._state.target_language
            }).raw

        return self._state

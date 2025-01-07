from crewai import Task
from agents.searcher_agent import searcher
from tools.search_tools import RAGSearchTool

search_tool = RAGSearchTool(result_as_answer=True)

# Create search task
search_task = Task(
    description="""Search through the literature database to verify the request_in_english and all the verification_facts. Based on the original request (in English), the verification_facts, and the questions, search for relevant articles that support or refute the claim:
       
    Your task is to:
    1. Create a list of search terms based on the original request, claims, questions and phrases composed by keywords and phrases
    2. Find relevant articles that support or refute the claim

    The user input to search is the following: '''{user_input}'''
    """,
    agent=searcher,
    expected_output="""The found fragments, with the textually repeated fragments eliminated and in an article format.""",
    tools=[search_tool]
)

from crewai import Task
from agents.internet_searcher_agent import internet_searcher
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

#SerperDevTool is a CrewAI´s builtin tool that allows to use Serper´s API to make searches over internet using Google
#ScrapeWebsiteTool is a CrewAI´s builtin tool based on python-request library thats implements basic web scraping

# Create search task
internet_search_task = Task(
    description="""Search through the internet, preferably using academic, professional or other reliables sources to verify the request_in_english and all the verification_facts. Based on the original request (in English), the verification_facts, and the questions, search for relevant articles that support or refute the claim:
       
    Your task is to:
    1. Make a search with SerperDevTool for at least 5 websites that contains relevant information.
    2. Scrape the most relevant websites with ScrapeWebsiteTool
    3. Return the most important fragment of each web site related to the topics on hand, textually, without modifications, along with the site url as source.

    The user input to search is the following: '''{user_input}'''
    """,
    agent=internet_searcher,
    expected_output="""Return the relevant information of each scraped web page, identifying it with the origin url. Structure the output as JSON, with each element as an object "content" (summary of the content of the web site, focused on the claims) and "internet_article_source" (containing the title of the article and the url).""",
    tools = [SerperDevTool(), ScrapeWebsiteTool()]
)

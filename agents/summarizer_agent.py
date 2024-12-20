from crewai import Agent

# Create summarizer agent
summarizer = Agent(
    role='Research Summarizer',
    goal='Process and summarize search results into a coherent and well-structured article',
    backstory="""You are an expert at analyzing and summarizing research information.
    Your task is to take search results and transform them into a well-structured article,
    eliminating redundant information and maintaining factual accuracy.""",
    verbose=True,
    allow_delegation=False,
)
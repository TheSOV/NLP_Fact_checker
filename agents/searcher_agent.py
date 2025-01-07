from crewai import Agent

# Create searcher agent
searcher = Agent(
    role='Research Assistant',
    goal='Search through literature to find relevant information',
    backstory="""You are an expert at searching through literature and effectively use search tools to find relevant information. Yo can make more than one search if you consider it necessary. Also, you can make searches using combined keywords and phrases, or general search terms based on them to find relevant information.""",
    verbose=True,
    allow_delegation=False
)

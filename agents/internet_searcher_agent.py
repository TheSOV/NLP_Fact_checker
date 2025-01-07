from crewai import Agent


# Create searcher agent
internet_searcher = Agent(
    role='Internet Research Assistant',
    goal='Search through Internet, in verified sources, like Academic Google, IEEE standards, and others, to find relevant information',
    backstory="""You are an expert at searching through verified or highly reliable sources in internet and effectively scrape the sources find relevant information.""",
    verbose=True,
    allow_delegation=False,
    
)

from crewai import Task
from agents.qa_agent import qa_agent
from tasks.search_task import search_task

# Create QA task
qa_task = Task(
    description="""Review and verify the fact verification response for proper referencing and accuracy:

    1. Check that every piece of information in the response is properly referenced:
       - Each fragment should be traceable to a specific source
       - Sources should be accurately cited
       - Wikipedia articles should match the search results
       - Other resources should be properly listed with URLs when available

    2. Verify the logical connection between:
       - Sources and fragments
       - Fragments and explanation
       - Explanation and classification

    3. If any information lacks proper referencing:
       - Identify the specific gaps
       - Delegate to the verifier agent for additional information
       - Request clarification or additional sources as needed

    4. Ensure the response follows the required format:
       - 1. Sources (Wikipedia articles) are textually cited from search results
       - 2. Fragments are properly quoted and linked to sources
       - 3. Explanation is based on cited fragments
       - 4. Classification is justified by the explanation
       - 5. Other resources are properly listed with URLs when available

    Important: If you find any issues, work with the verifier agent to resolve them before approving the response. You can also indicate to make more searches.""",
    agent=qa_agent,
    expected_output="""- 1. Sources (Wikipedia articles) are textually cited from search results
       - 2. Fragments are properly quoted and linked to sources
       - 3. Explanation is based on cited fragments
       - 4. Classification is justified by the explanation
       - 5. Other resources are properly listed with URLs when available""",
    context=[search_task]
)

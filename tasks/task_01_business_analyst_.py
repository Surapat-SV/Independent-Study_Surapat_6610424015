from crewai import Task

def create_business_analyst_tasks(senior_research_business_analyst, senior_writer_business_analyst, business_name, product_service, target_audience):
    # Research Task
    research_task = Task(
        description=f"""
            1. Search for the business '{business_name}' and gather:
                - Recent developments or news about the business
                - Product/service details and their market positioning
                - Information about the target audience '{target_audience}' and market trends
            2. Gain insights into business strategy and unique value propositions
            3. Evaluate the credibility of sources and fact-check all information
            4. Organize findings into a structured business analysis report
            5. Include citations and source references
        """,
        expected_output="""A structured business analysis report containing:
            - Business overview and recent updates
            - Detailed analysis of products/services
            - Insights into the target audience and market trends
            - Verified facts and data with citations
            - Summary of key findings and strategic recommendations
        """,
        agent=senior_research_business_analyst
    )

    # Writing Task
    writing_task = Task(
        description=f"""
            Based on the research provided, create a comprehensive business analysis report that:
            1. Provides a well-rounded understanding of the business
            2. Covers the product/service offering and its market positioning
            3. Discusses the target audience and market trends
            4. Includes:
                - An engaging introduction
                - Clear sections with appropriate headings
                - A conclusion summarizing key findings and strategic insights
            5. Maintains factual accuracy and proper citations in [Source: URL] format
            6. Formats the report using proper markdown, with H1 for the title and H3 for sections
        """,
        expected_output="""A polished business analysis report in markdown format that:
            - Is informative and well-structured
            - Includes inline citations linked to sources
            - Provides actionable insights for business improvement
            - Follows proper markdown formatting guidelines
        """,
        agent=senior_writer_business_analyst
    )

    return research_task, writing_task

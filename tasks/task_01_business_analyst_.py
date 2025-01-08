###############################################
# Business Analyst Tasks
# File: tasks/task_01_business_analyst_.py
# Purpose: Defines tasks for the Business Analyst agent to perform research and report writing
###############################################

# Import SQLite compatibility fix for GitHub environment
__import__('pysqlite3')  # Ensure SQLite works in certain environments
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')  # Replace sqlite3 with pysqlite3

# Import required libraries
import streamlit as st  # Streamlit for UI and secrets management
from crewai import Task  # CrewAI framework for task handling

# Function: Create Business Analyst Tasks
def create_business_analyst_tasks(senior_research_business_analyst, senior_writer_business_analyst, business_name, product_service, target_audience):
    """
    Creates and returns tasks for:
    1. Researching business details and market trends.
    2. Writing a comprehensive business analysis report.
    """

    # Task 1: Research Task
    research_task = Task(
        description=f"""
            Conduct research on the business '{business_name}' including:
            1. Recent developments or news about the business.
            2. Product/service details and market positioning.
            3. Target audience '{target_audience}' and market trends.
            4. Evaluate source credibility and fact-check all information.
            5. Organize findings into a structured business analysis report with citations.
        """,
        expected_output="""
            Structured business analysis report containing:
            - Business overview and recent updates.
            - Detailed analysis of products/services.
            - Target audience insights and market trends.
            - Verified facts and data with citations.
            - Strategic recommendations.
        """,
        agent=senior_research_business_analyst  # Assign to Research Agent
    )

    # Task 2: Writing Task
    writing_task = Task(
        description=f"""
            Transform research findings into a polished business analysis report that:
            1. Provides an in-depth understanding of the business.
            2. Covers product/service details and market positioning.
            3. Discusses target audience and market trends.
            4. Includes:
                - An engaging introduction.
                - Clear sections with headings.
                - A conclusion summarizing key findings and insights.
            5. Maintains factual accuracy and proper citations in [Source: URL] format.
            6. Uses markdown formatting (H1 for title, H3 for sections).
        """,
        expected_output="""
            Polished business analysis report in markdown format:
            - Informative and well-structured.
            - Inline citations linked to sources.
            - Actionable insights for business improvement.
            - Proper markdown formatting with titles and headings.
        """,
        agent=senior_writer_business_analyst  # Assign to Writer Agent
    )

    # Return both tasks
    return research_task, writing_task

# End of file: tasks/task_01_business_analyst_.py

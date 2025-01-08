###############################################
# Keyword Planner Agents
# File: agents/agent_03_keyword_planner.py
# Purpose: Defines AI agents for keyword planning and SEM optimization
###############################################

# Import required libraries
from crewai import Agent  # Core CrewAI framework for agents
from crewai_tools import QueryBigQueryTool  # Tool for connecting and querying BigQuery
import streamlit as st  # Streamlit for UI and interactive features

# Class: Keyword Planner Agents
class KeywordPlannerAgents:
    @staticmethod
    def keyword_planner_agent():
        """
        Defines the Keyword Planner agent responsible for:
        - Developing actionable keyword plans for SEM strategies
        - Analyzing keyword performance and trends
        - Providing optimization strategies including bidding and grouping
        """
        # Initialize BigQuery tool for database queries
        bigquery_tool = QueryBigQueryTool(
            project_id=st.secrets['BIGQUERY_PROJECT_ID'],  # Project ID from secrets
            credentials_path=st.secrets['BIGQUERY_CREDENTIALS_PATH']  # Credentials file path
        )

        # Create and return the Keyword Planner agent
        return Agent(
            role="Keyword Planner",  # Define the agent's role
            goal=(
                "Develop precise and actionable keyword plans for SEM strategies, leveraging BigQuery tools. "
                "Analyze keyword performance, trends, and relevance to identify opportunities and gaps in targeting. "
                "Provide optimization suggestions, including match types, bidding strategies, and ad group structures."
            ),
            backstory=(
                "An experienced Keyword Planner with expertise in database queries, SEM tools, and competitor analysis. "
                "Specializes in long-tail keyword identification, negative keyword management, and campaign optimization "
                "to maximize ROI. Combines analytical precision with creative strategy to develop data-driven keyword plans."
            ),
            tools=[bigquery_tool],  # Assign BigQuery tool for data queries
            verbose=True,  # Enable detailed logs for debugging
            memory=True,  # Enable memory to retain context between steps
            guardrails={
                'output_format': 'markdown',  # Ensure output format is Markdown
                'max_retries': 3,  # Maximum retry attempts
                'timeout': 300  # Timeout duration in seconds
            }
        )

# End of file: agents/agent_03_keyword_planner.py

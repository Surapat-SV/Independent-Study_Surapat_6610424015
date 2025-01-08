###############################################
# Keyword Planner Tasks
# File: tasks/task_03_keyword_planner.py
# Purpose: Defines tasks for keyword discovery, categorization, and trend analysis
###############################################

# Import required libraries
from crewai import Task  # Core CrewAI framework for tasks
from textwrap import dedent  # For multi-line string formatting
from crewai_tools import QueryBigQueryTool  # Tool for querying data from BigQuery

# Class: Keyword Planner Tasks
class KeywordPlannerTasks:

    def keyword_discovery_task(self, agent, query_input):
        """
        Task: Discover high-potential keywords for SEM strategies.
        Purpose: Analyze keyword relevance, search volume, and competition using BigQuery.
        """
        return Task(
            description=dedent(f"""
                Perform keyword discovery using BigQuery tools.
                Query databases for keywords related to the input topic and identify
                high-potential keywords based on relevance, search volume, and competition level.

                Analysis Steps:
                1. Fetch keyword data for '{query_input}' using BigQuery.
                2. Analyze metrics such as search volume, CPC, and competition.
                3. Rank keywords based on performance indicators.

                Tools Used:
                - BigQuery for keyword data retrieval and analysis.
            """),
            expected_output="A ranked list of keywords with metrics such as search volume, CPC, and competition levels.",
            agent=agent
        )

    def keyword_categorization_task(self, agent, keywords):
        """
        Task: Categorize discovered keywords into themes and match types.
        Purpose: Group keywords based on search intent and performance.
        """
        return Task(
            description=dedent(f"""
                Categorize keywords into themes and match types (Broad, Phrase, Exact).
                Group keywords based on intent, relevance, and performance metrics.

                Analysis Steps:
                1. Classify keywords by intent: informational, navigational, and transactional.
                2. Map each keyword to match types (Broad, Phrase, Exact) for targeting flexibility.
                3. Highlight primary and secondary keywords for campaign structuring.

                Tools Used:
                - BigQuery for keyword grouping and match-type classification.
            """),
            expected_output="Categorized keyword list with themes, match types, and targeting suggestions.",
            agent=agent
        )

    def keyword_trend_analysis_task(self, agent, keyword):
        """
        Task: Analyze keyword trends and seasonality patterns.
        Purpose: Evaluate growth trends and seasonal fluctuations using BigQuery.
        """
        return Task(
            description=dedent(f"""
                Analyze keyword trends using BigQuery to track changes over time.
                Evaluate search volume, growth trends, and seasonality patterns.

                Analysis Steps:
                1. Retrieve trend data for '{keyword}' from BigQuery.
                2. Analyze short-term and long-term changes in search volume.
                3. Provide insights into seasonal fluctuations and emerging trends.

                Tools Used:
                - BigQuery for keyword trend analysis.
            """),
            expected_output="Keyword trend analysis report highlighting growth trends and seasonality insights.",
            agent=agent
        )

# End of file: tasks/task_03_keyword_planner.py

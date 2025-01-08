###############################################
# Keyword Planner Page
# File: pages/page_03_keyword_planner.py
# Purpose: Provides Streamlit interface for Keyword Planner tasks
###############################################

# Import SQLite compatibility fix for GitHub environment
__import__('pysqlite3')  # Ensure SQLite works in certain environments
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')  # Replace sqlite3 with pysqlite3

# Import required libraries
import streamlit as st  # Streamlit for UI handling
from crewai import Crew  # CrewAI framework for handling agents and tasks
from agents.agent_03_keyword_planner import KeywordPlannerAgents  # Import Keyword Planner agents
from tasks.task_03_keyword_planner import KeywordPlannerTasks  # Import Keyword Planner tasks

# Function: Run Keyword Planner Page
def run_keyword_planner():
    """
    Streamlit interface for Keyword Planner tasks:
    - Allows users to input keywords for analysis.
    - Generates keyword plans based on SEM strategies.
    """
    # Page Title
    st.title("🔑 Keyword Planner")
    st.markdown("Create and analyze keyword plans to optimize your SEM campaigns.")

    # Collect user input
    query_input = st.text_input(
        "Enter Keywords or Topics:", placeholder="Enter keywords or topics to analyze."
    )

    # Generate Keyword Plan Button
    if st.button("Generate Keyword Plan"):
        # Validate inputs
        if query_input:
            try:
                # Step 1: Initialize agents and tasks
                agents = KeywordPlannerAgents()
                tasks = KeywordPlannerTasks()
                keyword_planner = agents.keyword_planner_agent()

                # Step 2: Create tasks for keyword discovery and categorization
                discovery_task = tasks.keyword_discovery_task(keyword_planner, query_input)
                categorization_task = tasks.keyword_categorization_task(keyword_planner, [query_input])
                trend_task = tasks.keyword_trend_analysis_task(keyword_planner, query_input)

                # Step 3: Create Crew and execute tasks
                crew = Crew(
                    agents=[keyword_planner],
                    tasks=[discovery_task, categorization_task, trend_task],
                    verbose=True,
                )
                results = crew.kickoff()

                # Step 4: Display results
                st.subheader("Keyword Plan Report")
                for i, result in enumerate(results):
                    st.markdown(f"### Task {i + 1} Output")
                    st.write(result)

                # Key Recommendations
                st.subheader("Key Recommendations")
                st.markdown("""
                - **Focus on Keyword Gaps:** Target missing keywords for SEM improvement.
                - **Use Negative Keywords:** Reduce irrelevant traffic and ad spend.
                - **Ad Group Structuring:** Group keywords into themes for targeted ads.
                - **Optimize Metadata:** Enhance descriptions and headlines based on findings.
                """)

            except Exception as e:
                st.error(f"An error occurred while generating the keyword plan: {str(e)}")
        else:
            # Warning if inputs are incomplete
            st.warning("Please provide keywords or topics for analysis.")

# End of file: pages/page_03_keyword_planner.py

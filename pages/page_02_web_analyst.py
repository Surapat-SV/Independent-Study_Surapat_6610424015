###############################################
# Web Analyst Page
# File: pages/page_02_web_analyst.py
# Purpose: Provides Streamlit interface for Web Analyst tasks
###############################################

# Import SQLite compatibility fix for GitHub environment
__import__('pysqlite3')  # Ensure SQLite works in certain environments
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')  # Replace sqlite3 with pysqlite3

# Import required libraries
import streamlit as st  # Streamlit for UI handling
from crewai import Crew  # CrewAI framework for handling agents and tasks
from agents.agent_02_website_analyst import WebsiteAnalystAgents  # Import agents
from tasks.task_02_website_analyst import WebsiteAnalystTasks  # Import tasks

# Function: Run Web Analyst Page
def run_web_analyst():
    """
    Streamlit interface for Web Analyst tasks:
    - Allows users to input website URLs.
    - Analyzes metadata and keywords for SEO optimization.
    """
    # Page Title
    st.title("🌐 Web Analyst")

    # Collect user input
    our_url = st.text_input("Enter your website URL:", placeholder="https://www.ourwebsite.com")
    competitor_url = st.text_input("Enter competitor's website URL:", placeholder="https://www.competitor.com")

    # Analyze Button
    if st.button("Analyze Websites"):
        # Validate inputs
        if our_url and competitor_url:
            try:
                # Step 1: Create agents and tasks
                agents = WebsiteAnalystAgents()
                tasks = WebsiteAnalystTasks()
                agent = agents.web_analyst_agent()
                analysis_task = tasks.website_analysis_task(agent, our_url, competitor_url)

                # Step 2: Execute task
                crew = Crew(agents=[agent], tasks=[analysis_task], verbose=True)
                results = crew.kickoff()

                # Step 3: Display results
                st.subheader("Analysis Results")
                for result in results:
                    st.markdown(result)

                # Key Recommendations
                st.subheader("Key Insights and Recommendations")
                st.markdown("""
                - **Optimize Metadata:** Update titles and descriptions for better SEO.
                - **Keyword Optimization:** Focus on high-performing keywords.
                - **Improve Content Structure:** Ensure content aligns with target keywords.
                """)

            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")
        else:
            # Warning if inputs are incomplete
            st.warning("Please provide both URLs for analysis.")

# End of file: pages/page_02_web_analyst.py

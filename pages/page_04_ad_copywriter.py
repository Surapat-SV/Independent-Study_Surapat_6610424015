###############################################
# Ad Copywriter Page
# File: pages/page_04_ad_copywriter.py
# Purpose: Provides Streamlit interface for generating SEM text ads
###############################################

# Import SQLite compatibility fix for GitHub environment
__import__('pysqlite3')  # Ensure SQLite works in certain environments
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')  # Replace sqlite3 with pysqlite3

# Import required libraries
import streamlit as st  # Streamlit for UI handling
from crewai import Crew  # CrewAI framework for handling agents and tasks
from agents.agent_04_adcopywriter import AdcopyWriterAgents  # Import Ad Copywriter agents
from tasks.task_04_adcopy_writer import AdCopyWriterTasks  # Import Ad Copywriter tasks

# Function: Run Ad Copywriter Page
def run_ad_copywriter():
    """
    Streamlit interface for Ad Copywriter tasks:
    - Generates SEM text ads with headlines and descriptions.
    """
    # Page Title
    st.title("✍️ Ad Copywriter")
    st.markdown("Generate compelling Google Ads text, including headlines and descriptions, for SEM campaigns.")

    # Button to trigger text ad generation
    if st.button("Generate Text Ads"):
        try:
            # Step 1: Initialize agents and tasks
            agents = AdcopyWriterAgents()
            tasks = AdCopyWriterTasks()
            ad_copywriter = agents.adcopy_writer_agent()

            # Step 2: Create Ad Copywriting Task
            ad_copywriter_task = tasks.ad_copywriter_task(ad_copywriter)

            # Step 3: Create Crew and execute tasks
            crew = Crew(
                agents=[ad_copywriter],
                tasks=[ad_copywriter_task],
                verbose=True
            )
            result = crew.kickoff()

            # Step 4: Display Results
            st.subheader("Generated Text Ads")

            # Display headlines
            st.markdown("### Headlines:")
            for i, headline in enumerate(result.get('headlines', []), start=1):
                st.write(f"{i}. {headline}")

            # Display descriptions
            st.markdown("### Descriptions:")
            for i, description in enumerate(result.get('descriptions', []), start=1):
                st.write(f"{i}. {description}")

        except Exception as e:
            # Handle errors
            st.error(f"An error occurred while generating text ads: {str(e)}")

# End of file: pages/page_04_ad_copywriter.py

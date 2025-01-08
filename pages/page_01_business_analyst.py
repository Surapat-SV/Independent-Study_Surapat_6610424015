###############################################
# Business Analyst Page
# File: pages/page_01_business_analyst.py
# Purpose: Provides Streamlit interface for Business Analyst tasks
###############################################

# Import SQLite compatibility fix for GitHub environment
__import__('pysqlite3')  # Ensure SQLite works in certain environments
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')  # Replace sqlite3 with pysqlite3

# Import required libraries
import streamlit as st  # Streamlit for UI handling
from crewai import Crew  # CrewAI framework for handling agents and tasks

# Import Business Analyst agents and tasks
from src.agents.agent_01_business_analyst import create_business_analyst_agents
from tasks.task_01_business_analyst import create_business_analyst_tasks

# Function: Run Business Analyst Page
def run_business_analyst():
    """
    Streamlit interface for Business Analyst tasks:
    - Allows users to input business details.
    - Generates business analysis report based on inputs.
    """
    # Page Title
    st.title("📋 Business Analyst")

    # Collect user input
    business_name = st.text_input("Enter the business name:")
    product_service = st.text_area("Describe the product or service:")
    target_audience = st.text_area("Describe the target audience:")

    # Generate Business Analysis Button
    if st.button("Generate Business Analysis"):
        # Validate inputs
        if business_name and product_service and target_audience:
            # Step 1: Create agents for research and writing tasks
            senior_research_business_analyst, senior_writer_business_analyst = create_business_analyst_agents()

            # Step 2: Create tasks using the agents
            research_task, writing_task = create_business_analyst_tasks(
                senior_research_business_analyst,
                senior_writer_business_analyst,
                business_name,
                product_service,
                target_audience
            )

            # Step 3: Display task descriptions
            st.subheader("Research Task Description")
            st.markdown(research_task.description)  # Show research task details

            st.subheader("Writing Task Description")
            st.markdown(writing_task.description)  # Show writing task details

            # Step 4: Execute tasks
            crew = Crew(agents=[senior_research_business_analyst, senior_writer_business_analyst], tasks=[research_task, writing_task])
            results = crew.kickoff()

            # Step 5: Display results
            st.subheader("Generated Business Analysis Report")
            for result in results:
                st.markdown(result)

        else:
            # Warning if inputs are incomplete
            st.warning("Please fill in all fields before generating the analysis.")

# End of file: pages/page_01_business_analyst.py

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from crewai import Crew
from agents.website_analyst_agents import WebsiteAnalystAgents, StreamToExpander
from tasks.website_analyst_tasks import WebsiteAnalystTasks
from agents.keyword_planner_agents import KeywordPlannerAgents, StreamToExpander
from tasks.keyword_planner_tasks import KeywordPlannerTasks
import streamlit as st
import datetime
import sys

def run_keyword_planner():
    """
    Displays the Keyword Planner page where users can input keywords or topics to analyze.
    """
    # Set up the header and UI
    st.header("Keyword Planner")
    st.markdown("Create and analyze keyword plans to optimize your SEM campaigns.")

    # Input fields
    query_input = st.text_input(
        "Keyword Query Input:", placeholder="Enter keywords or topics to analyze."
    )
    competitor_url = st.text_input(
        "Competitor Website URL:", placeholder="Enter competitor's website URL (Optional)."
    )

    # Button to generate Keyword Planner
    if st.button("Generate Keyword Plan"):
        # Display processing status
        with st.status("🔍 **Generating Keyword Plan...**", state="running", expanded=True) as status:
            with st.container(height=500, border=False):
                # Initialize output logger
                sys.stdout = StreamToExpander(st)

                try:
                    # Initialize agents and tasks
                    agents = KeywordPlannerAgents()
                    tasks = KeywordPlannerTasks()

                    # Create agents
                    keyword_planner = agents.keyword_planner_agent()
                    competitor_analyst = agents.web_analyst_agent()

                    # Create tasks
                    keyword_discovery_task = tasks.keyword_discovery_task(keyword_planner, query_input)
                    keyword_categorization_task = tasks.keyword_categorization_task(keyword_planner, [query_input])

                    # Optional: Competitor Analysis if URL is provided
                    competitor_analysis_task = None
                    if competitor_url:
                        competitor_analysis_task = tasks.keyword_competitor_analysis_task(
                            competitor_analyst, query_input, competitor_url
                        )

                    # Negative Keyword Task
                    negative_keywords_task = tasks.negative_keyword_identification_task(keyword_planner, [query_input])

                    # Grouping and Mapping Task
                    keyword_grouping_task = tasks.keyword_grouping_task(keyword_planner, [query_input])

                    # Final Report Task
                    final_report_task = tasks.final_keyword_planner_task(keyword_planner)

                    # Create crew and execute tasks
                    crew_tasks = [
                        keyword_discovery_task,
                        keyword_categorization_task,
                        negative_keywords_task,
                        keyword_grouping_task,
                        final_report_task,
                    ]

                    # Add competitor analysis task if available
                    if competitor_analysis_task:
                        crew_tasks.insert(2, competitor_analysis_task)

                    # Initialize the crew
                    crew = Crew(
                        agents=[keyword_planner, competitor_analyst],
                        tasks=crew_tasks,
                        verbose=True,
                    )

                    # Execute tasks
                    results = crew.kickoff()
                    status.update(label="✅ Keyword Plan Ready!", state="complete", expanded=False)

                    # Display Results
                    st.subheader("Keyword Plan Report")
                    for i, result in enumerate(results):
                        st.markdown(f"### Task {i + 1} Output")
                        st.write(result)

                    # Additional Insights
                    st.subheader("Key Recommendations")
                    st.markdown("""
                    - **Focus on Keyword Gaps:** Optimize SEM performance by targeting missing keywords.
                    - **Use Negative Keywords:** Filter irrelevant traffic and reduce ad spend.
                    - **Ad Group Structuring:** Group keywords into tightly themed groups for targeted ads.
                    - **Optimize Metadata:** Enhance ad copy and descriptions based on findings.
                    """)

                except Exception as e:
                    # Handle errors gracefully
                    st.error(f"An error occurred while generating the keyword plan: {str(e)}")

    # Clear session data
    if st.button("Clear Inputs"):
        st.session_state.clear()
        st.rerun()

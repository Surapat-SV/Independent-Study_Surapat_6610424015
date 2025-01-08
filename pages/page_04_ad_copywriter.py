__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from crewai import Crew
from agents.adcopy_writer_agents import AdcopyWriterAgents
from tasks.adcopy_writer_tasks import AdCopyWriterTasks
import streamlit as st
import datetime
import sys

def run_ad_copywriter():
    """
    Displays the Ad Copywriter page where users can generate SEM text ads.
    """
    # Header and description
    st.header("Ad Copywriter")
    st.markdown("Generate compelling Google Ads text, including headlines and descriptions, for SEM campaigns.")

    # Button to trigger text ad generation
    if st.button("Generate Text Ads"):
        # Display status indicator while generating ads
        with st.status("✍️ **Generating Text Ads...**", state="running", expanded=True) as status:
            with st.container(height=500, border=False):
                # Initialize output logger
                sys.stdout = StreamToExpander(st)

                try:
                    # Initialize agents and tasks
                    agents = AdcopyWriterAgents()
                    tasks = AdCopyWriterTasks()

                    # Create ad copywriter agent and task
                    ad_copywriter = agents.adcopy_writer_agent()
                    ad_copywriter_task = tasks.ad_copywriter_task(ad_copywriter)

                    # Combine agents and tasks into a crew
                    crew = Crew(
                        agents=[ad_copywriter],
                        tasks=[ad_copywriter_task],
                        verbose=True
                    )

                    # Execute tasks
                    result = crew.kickoff()
                    status.update(label="✅ Text Ads Ready!", state="complete", expanded=False)

                    # Display Results
                    st.subheader("Generated Text Ads", anchor=False, divider="rainbow")

                    # Parse and format the results
                    st.markdown("### Headlines:")
                    if isinstance(result, dict) and 'headlines' in result:
                        for i, headline in enumerate(result['headlines'], start=1):
                            st.write(f"{i}. {headline}")
                    else:
                        st.write("No headlines were generated.")

                    st.markdown("### Descriptions:")
                    if isinstance(result, dict) and 'descriptions' in result:
                        for i, description in enumerate(result['descriptions'], start=1):
                            st.write(f"{i}. {description}")
                    else:
                        st.write("No descriptions were generated.")

                except Exception as e:
                    # Error handling
                    st.error(f"An error occurred while generating text ads: {str(e)}")

    # Clear session data
    if st.button("Clear Inputs"):
        st.session_state.clear()
        st.rerun()

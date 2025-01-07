__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from crewai import Crew
from agents.business_analyst_agents import BusinessAnalystAgents, StreamToExpander
from tasks.business_analyst_tasks import BusinessAnalystTasks
import streamlit as st
import datetime
import uuid

# Chatbot Avatar
avatar_assistant = "BA-icon.png"

# Define the Business Analyst Chatbot Function
def run_business_analyst():
    # Initialize session state for messages and context
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    if "context" not in st.session_state:
        st.session_state["context"] = {}

    if "thread_id" not in st.session_state:
        st.session_state["thread_id"] = str(uuid.uuid4())

    # Display chat history
    for msg in st.session_state["messages"]:
        if msg["role"] == "assistant":
            st.chat_message(msg["role"], avatar=avatar_assistant).write(msg["content"])
        else:
            st.chat_message(msg["role"]).write(msg["content"])

    # Chat input
    user_input = st.chat_input(placeholder="Ask a question or answer the Assistant")
    if user_input:
        # Append user input to session state
        st.session_state["messages"].append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        try:
            # Initialize conversational agent
            agent = BusinessAnalystAgents.conversational_business_analyst_agent()

            # Update context with new user input
            st.session_state["context"]["last_input"] = user_input

            # Define the task with current context
            task = BusinessAnalystTasks().conversational_gathering_task(agent, st.session_state["context"])

            # Create a Crew
            crew = Crew(agents=[agent], tasks=[task], verbose=True)

            # Execute the task
            results = crew.kickoff()

            # Ensure output format
            if isinstance(results, list) and len(results) > 0:
                result_message = results[0]
            else:
                result_message = str(results)

            # Update context with output
            st.session_state["context"]["last_output"] = result_message

            # Append assistant response
            st.session_state["messages"].append({"role": "assistant", "content": result_message})
            st.chat_message("assistant", avatar=avatar_assistant).write(result_message)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # Clear history button
    if st.button("Clear Chat History"):
        st.session_state.clear()
        st.rerun()

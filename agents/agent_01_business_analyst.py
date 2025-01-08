###############################################
# Business Analyst Agents
# File: agents/agent_01_business_analyst.py
# Purpose: Defines AI agents for business research and report generation
###############################################

# Import SQLite compatibility fix for GitHub environment
__import__('pysqlite3')  # Ensure SQLite works in certain environments
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')  # Replace sqlite3 with pysqlite3

# Import required libraries
import streamlit as st  # Streamlit for UI and secrets management
import os  # OS module for environment handling
from crewai import Agent, LLM  # CrewAI for agent and LLM handling
from crewai_tools import SerperDevTool  # Tools for web search integration

# Function to create Business Analyst Agents
def create_business_analyst_agents():
    """
    Initializes and returns two agents:
    1. Senior Research Business Analyst - Conducts detailed research
    2. Senior Writer Business Analyst - Creates business analysis reports
    """

    # Step 1: Load API keys securely from Streamlit secrets
    serper_api_key = st.secrets['SERPER_API_KEY']  # Serper API key for search
    gemini_api_key = st.secrets['GEMINI_API_KEY']  # Gemini API key for LLM

    # Step 2: Initialize the Language Model (LLM) using Google Gemini 1.5 Flash
    llm = LLM(
        model="gemini/gemini-1.5-flash",  # Model version
        api_key=gemini_api_key,  # API key for authentication
        temperature=0.1  # Control randomness (0.1 = more deterministic)
    )

    # Step 3: Initialize SerperDevTool for web search functionality
    search_tool = SerperDevTool(
        api_key=serper_api_key,  # API key for SerperDevTool
        n_results=4  # Number of results to fetch
    )

    # Step 4: Define the Senior Research Business Analyst Agent
    senior_research_business_analyst = Agent(
        role="Senior Research Business Analyst",  # Agent role
        goal=(
            "Conduct in-depth research on businesses, products/services, "
            "and target audiences."
        ),
        backstory=(
            "Experienced business analyst who excels at researching businesses "
            "and synthesizing insights."
        ),
        allow_delegation=False,  # Disable delegation to other agents
        verbose=True,  # Enable detailed logs
        tools=[search_tool],  # Assign search tool for data gathering
        llm=llm  # Assign language model for processing
    )

    # Step 5: Define the Senior Writer Business Analyst Agent
    senior_writer_business_analyst = Agent(
        role="Senior Writer Business Analyst",  # Agent role
        goal=(
            "Transform business research into clear and compelling business "
            "analysis reports."
        ),
        backstory=(
            "Skilled content writer who creates clear and actionable reports "
            "based on business research."
        ),
        allow_delegation=False,  # Disable delegation to other agents
        verbose=True,  # Enable detailed logs
        llm=llm  # Assign language model for processing
    )

    # Step 6: Return both agents for use in tasks
    return senior_research_business_analyst, senior_writer_business_analyst

# End of file: agents/agent_01_business_analyst.py

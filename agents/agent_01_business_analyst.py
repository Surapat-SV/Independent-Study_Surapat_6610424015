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
from crewai import Agent, LLM  # CrewAI for agent and LLM handling
from crewai_tools import SerperDevTool  # Tools for web search integration

# Class: Business Analyst Agents
class BusinessAnalystAgents:
    """
    Initializes Business Analyst agents for:
    1. Researching businesses, products, and target audiences.
    2. Generating structured business analysis reports.
    """

    def __init__(self):
        """
        Initialize API keys and LLM configurations.
        """
        # Load API keys securely from Streamlit secrets
        self.serper_api_key = st.secrets['SERPER_API_KEY']  # Serper API key for search
        self.gemini_api_key = st.secrets['GEMINI_API_KEY']  # Gemini API key for LLM

        # Initialize Language Model (LLM) using Google Gemini 1.5 Flash
        self.llm = LLM(
            model="gemini/gemini-1.5-flash",  # Model version
            api_key=self.gemini_api_key,  # API key for authentication
            temperature=0.1  # Control randomness (0.1 = more deterministic)
        )

        # Initialize SerperDevTool for web search functionality
        self.search_tool = SerperDevTool(
            api_key=self.serper_api_key,  # API key for SerperDevTool
            n_results=4  # Number of results to fetch
        )

    def create_agents(self):
        """
        Creates and returns two agents:
        1. Senior Research Business Analyst
        2. Senior Writer Business Analyst
        """

        # Define the Senior Research Business Analyst Agent
        senior_research_business_analyst = Agent(
            role="Senior Research Business Analyst",  # Agent role
            goal="Conduct in-depth research on businesses, products/services, and target audiences.",
            backstory="Experienced analyst specializing in researching businesses and synthesizing insights.",
            allow_delegation=False,  # Disable delegation to other agents
            verbose=True,  # Enable detailed logs
            tools=[self.search_tool],  # Assign search tool for data gathering
            llm=self.llm  # Assign language model for processing
        )

        # Define the Senior Writer Business Analyst Agent
        senior_writer_business_analyst = Agent(
            role="Senior Writer Business Analyst",  # Agent role
            goal="Transform business research into clear and compelling business analysis reports.",
            backstory="Expert writer skilled at creating structured and actionable reports.",
            allow_delegation=False,  # Disable delegation to other agents
            verbose=True,  # Enable detailed logs
            llm=self.llm  # Assign language model for processing
        )

        # Return the two agents
        return senior_research_business_analyst, senior_writer_business_analyst

# End of file: agents/agent_01_business_analyst.py

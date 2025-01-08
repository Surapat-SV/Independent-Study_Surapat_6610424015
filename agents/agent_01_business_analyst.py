from crewai import Agent
from langchain_community.llms import LLM
from tools.search_tools import SerperDevTool
import streamlit as st

def create_business_analyst_agents():
    # Access API keys from st.secrets
    serper_api_key = st.secrets['SERPER_API_KEY']
    gemini_api_key = st.secrets['GEMINI_API_KEY']

    # Initialize LLM with Google Gemini 1.5 Flash
    llm = LLM(
        model="gemini/gemini-1.5-flash",
        api_key=gemini_api_key,
        temperature=0.7
    )

    # Initialize SerperDevTool with Serper API key
    search_tool = SerperDevTool(api_key=serper_api_key, n_results=4)

    # First Agent: Senior Research Business Analyst
    senior_research_business_analyst = Agent(
        role="Senior Research Business Analyst",
        goal="Conduct in-depth research on businesses, products/services, and target audiences.",
        backstory="Experienced business analyst who excels at researching businesses and synthesizing insights.",
        allow_delegation=False,
        verbose=True,
        tools=[search_tool],
        llm=llm
    )

    # Second Agent: Senior Writer Business Analyst
    senior_writer_business_analyst = Agent(
        role="Senior Writer Business Analyst",
        goal="Transform business research into clear and compelling business analysis reports.",
        backstory="Skilled content writer who creates clear and actionable reports based on business research.",
        allow_delegation=False,
        verbose=True,
        llm=llm
    )

    return senior_research_business_analyst, senior_writer_business_analyst

###############################################
# Website Analyst Agents
# File: agents/agent_02_website_analyst.py
# Purpose: Defines AI agents for website analysis and SEO optimization
###############################################

# Import required libraries
from crewai import Agent  # Core CrewAI framework for agents
from crewai_tools import SerperDevTool, ScrapeWebsiteTool  # Tools for web search and scraping
import streamlit as st  # Streamlit for UI and interactive features

# Class: Website Analyst Agents
class WebsiteAnalystAgents:
    @staticmethod
    def web_analyst_agent():
        """
        Defines the Website Data Analyst agent responsible for:
        - Searching and scraping website metadata
        - Extracting keywords and analyzing SEO performance
        - Providing insights for competitive benchmarking
        """
        # Initialize tools
        search_tool = SerperDevTool(api_key=st.secrets['SERPER_API_KEY'], n_results=5)  # Search tool for web content
        scrape_tool = ScrapeWebsiteTool()  # Scraping tool for extracting website data

        # Create and return the agent
        return Agent(
            role="Website Data Analyst",  # Define the agent's role
            goal=(
                "Search, scrape, and analyze metadata, keywords, and SEO performance of websites. "
                "Provide insights for optimization and competitive benchmarking."
            ),
            backstory=(
                "An expert Website Data Analyst with advanced search and scraping tools for SEO optimization "
                "and competitive analysis."
            ),
            tools=[search_tool, scrape_tool],  # Add tools for web search and scraping
            allow_delegation=True,  # Allows delegation of tasks to other agents
            memory=True,  # Enables memory for storing context between steps
            verbose=True,  # Provides detailed logs for debugging
            guardrails={
                'output_format': 'markdown',  # Ensure output format is Markdown
                'max_retries': 3,  # Maximum retry attempts
                'timeout': 300  # Timeout duration in seconds
            }
        )

# End of file: agents/agent_02_website_analyst.py

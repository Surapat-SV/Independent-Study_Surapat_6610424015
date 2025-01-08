from crewai import Agent
from langchain_community.llms import OpenAI
from tools.search_tools import SearchTools
from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.bs4scrape_tools import ScrapeTools
from tools.querygbq_tools import BigQueryTools
import re
import streamlit as st

# Class: Keyword Planner Agents
class KeywordPlannerAgents:
    @staticmethod
    def keyword_planner_agent():
        """
        Defines the Keyword Planner agent responsible for developing actionable keyword plans,
        analyzing keyword performance, and providing optimization strategies.
        """
        return Agent(
            role="Keyword Planner",
            goal=(
                "Develop precise and actionable keyword plans for SEM strategies, leveraging BigQuery and web scraping tools. "
                "Analyze keyword performance, trends, and relevance to identify opportunities and gaps in targeting. "
                "Provide optimization suggestions, including match types, bidding strategies, and ad group structures."
            ),
            backstory=(
                "An experienced Keyword Planner with over 15 years of expertise in database queries, SEM tools, and competitor analysis. "
                "Specializes in long-tail keyword identification, negative keyword management, and campaign optimization to maximize ROI. "
                "Combines analytical precision with creative strategy to develop data-driven keyword plans tailored to client needs."
            ),
            tools=[
                BigQueryTools.run_bigquery  # Added BigQuery tool for data queries
            ],
            verbose=True,
            memory=True,
            guardrails={
                'output_format': 'markdown',
                'max_retries': 3,
                'timeout': 300
            }
        )


###########################################################################################
# Print agent process to Streamlit app container                                          #
###########################################################################################
class StreamToExpander:
    def __init__(self, expander):
        self.expander = expander
        self.buffer = []
        self.colors = ['red', 'green', 'blue', 'orange']  # Define a list of colors
        self.color_index = 0  # Initialize color index

    def write(self, data):
        # Filter out ANSI escape codes using a regular expression
        cleaned_data = re.sub(r'\x1B\[[0-9;]*[mK]', '', data)

        # Check if the data contains 'task' information
        task_match_object = re.search(r'"task"\s*:\s*"(.*?)"', cleaned_data, re.IGNORECASE)
        task_match_input = re.search(r'task\s*:\s*([^\n]*)', cleaned_data, re.IGNORECASE)
        task_value = None
        if task_match_object:
            task_value = task_match_object.group(1)
        elif task_match_input:
            task_value = task_match_input.group(1).strip()

        if task_value:
            st.toast(":robot_face: " + task_value)

        # Check if the text contains the specified phrase and apply color
        if "Entering new CrewAgentExecutor chain" in cleaned_data:
            self.color_index = (self.color_index + 1) % len(self.colors)
            cleaned_data = cleaned_data.replace("Entering new CrewAgentExecutor chain", f":{self.colors[self.color_index]}[Entering new CrewAgentExecutor chain]")

        # Update agent names to reflect the new class structure
        agent_mapping = {
            "Business Analyst": "Business Analyst Agent",
            "Website Data Analyst": "Website Analyst Agent",
            "Keyword Planner": "Keyword Planner Agent",
            "Lead Ad Copy Writer": "Ad Copywriter Agent"
        }

        for old_name, new_name in agent_mapping.items():
            if old_name in cleaned_data:
                cleaned_data = cleaned_data.replace(old_name, f":{self.colors[self.color_index]}[{new_name}]")

        if "Finished chain." in cleaned_data:
            cleaned_data = cleaned_data.replace("Finished chain.", f":{self.colors[self.color_index]}[Finished chain.]")

        self.buffer.append(cleaned_data)
        if "\n" in data:
            self.expander.markdown(''.join(self.buffer), unsafe_allow_html=True)
            self.buffer = []

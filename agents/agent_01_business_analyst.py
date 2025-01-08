from crewai import Agent
from langchain_community.llms import OpenAI
from tools.search_tools import SearchTools
from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.bs4scrape_tools import ScrapeTools
from tools.querygbq_tools import BigQueryTools
import re
import streamlit as st


# Class: Business Analyst Agents
class BusinessAnalystAgents:
    @staticmethod
    def business_analyst_agent():
        return Agent(
            role="Business Analyst",
            goal="Ask strategic questions to help define the target audience and gather detailed business requirements.",
            backstory=(
                "You are a skilled Business Analyst with expertise in identifying target audiences and clarifying business goals. "
                "Your primary responsibility is to gather requirements by asking targeted questions about the product or service. "
                "You collaborate with stakeholders to ensure their needs are fully understood and documented. "
                "Your insights serve as the foundation for planning marketing strategies and campaigns."
            ),
            allow_delegation=False,
            verbose=True
        )

    @staticmethod
    def conversational_business_analyst_agent():
        """
        Conversational Business Analyst AI Agent for gathering business information interactively.
        """
        return Agent(
            role="Conversational Business Analyst",
            goal=(
                "Engage in a structured conversation with the user to gather detailed information about their "
                "business, including name, products/services, target audience, unique value proposition, and goals."
            ),
            backstory=(
                "You are an expert Business Analyst who specializes in asking strategic questions to uncover "
                "business details. Your task is to interact with users through dynamic questioning and provide "
                "guidance on clarifying their marketing strategies."
            ),
            verbose=True,
            memory=True,
            allow_delegation=False
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

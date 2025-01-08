###############################################
# SEM Planner - AI Powered App
# File: streamlit_app.py
# Purpose: Main entry point for the SEM Planner application.
###############################################

# Ensure compatibility for SQLite in certain environments
__import__('pysqlite3')  # Fix SQLite compatibility for Streamlit
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# Import required libraries
from crewai import Crew  # CrewAI framework for agents and tasks
from streamlit_option_menu import option_menu  # Sidebar navigation menu
import streamlit as st  # Streamlit for UI rendering

# Import modularized Agents
from agents.agent_01_business_analyst import BusinessAnalystAgents
from agents.agent_02_website_analyst import WebsiteAnalystAgents
from agents.agent_03_keyword_planner import KeywordPlannerAgents
from agents.agent_04_adcopywriter import AdcopyWriterAgents

# Import modularized Tasks
from tasks.task_01_business_analyst import BusinessAnalystTasks
from tasks.task_02_website_analyst import WebsiteAnalystTasks
from tasks.task_03_keyword_planner import KeywordPlannerTasks
from tasks.task_04_adcopy_writer import AdCopyWriterTasks

# Import views for modular UI handling
from pages.page_01_business_analyst import run_business_analyst
from pages.page_02_web_analyst import run_web_analyst
from pages.page_03_keyword_planner import run_keyword_planner
from pages.page_04_ad_copywriter import run_ad_copywriter

# Configure Streamlit page settings
st.set_page_config(
    layout="wide",  # Wide layout for better content visibility
    initial_sidebar_state="expanded",  # Expanded sidebar by default
    page_title="SEM Planner - AI Powered App",  # Page title
    page_icon="🧠"  # Icon for the app
)

# Sidebar Header and App Info
st.sidebar.title("SEM Planner - AI Powered App")
st.sidebar.info(
    """
    Plan and Optimize SEM Campaigns:
    - 📋 Define Target Audience
    - 🌐 Analyze Websites and Keywords
    - 🔑 Optimize Keyword Strategies
    - ✍️ Generate Ad Copies
    """
)

# Sidebar Menu for Navigation
with st.sidebar:
    selected = option_menu(
        "Navigation Menu",  # Menu title
        ["Business Analyst", "Web Analyst", "Keyword Planner", "Ad Copywriter"],  # Menu options
        icons=["briefcase", "globe", "key", "pencil"],  # Icons for each menu item
        default_index=0  # Default selection
    )

# Route to the selected module based on the menu selection
if selected == "Business Analyst":
    st.header("📋 Business Analyst")
    run_business_analyst()

elif selected == "Web Analyst":
    st.header("🌐 Web Analyst")
    run_web_analyst()

elif selected == "Keyword Planner":
    st.header("🔑 Keyword Planner")
    run_keyword_planner()

elif selected == "Ad Copywriter":
    st.header("✍️ Ad Copywriter")
    run_ad_copywriter()

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Developed by AI Engineer | Powered by Streamlit & CrewAI")

# End of file: streamlit_app.py

# Ensure compatibility for SQLite in certain environments
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# Import core libraries
from crewai import Crew
from streamlit_option_menu import option_menu
import streamlit as st

# Import modularized Agents
from agent_01_business_analyst import BusinessAnalystAgents
from agent_02_business_analyst import WebsiteAnalystAgents
from agent_03_business_analyst import KeywordPlannerAgents
from agent_04_business_analyst import  AdCopyWriterAgents

# Import modularized Tasks
from task_01_business_analyst import BusinessAnalystTasks
from task_02_business_analyst import WebsiteAnalystTasks
from task_03_business_analyst import KeywordPlannerTasks
from task_04_business_analyst import  AdCopyWriterTasks

# Import views for modular UI handling
from pages.business_analyst import run_business_analyst
from pages.web_analyst import run_web_analyst
from pages.keyword_planner import run_keyword_planner
from pages.ad_copywriter import run_ad_copywriter

# Set Streamlit page configuration
st.set_page_config(
    layout="wide", 
    initial_sidebar_state="expanded", 
    page_title="SEM Planner - AI Powered App", 
    page_icon="🧠"
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

# Sidebar Menu
with st.sidebar:
    selected = option_menu(
        "Navigation Menu",
        ["Business Analyst", "Web Analyst", "Keyword Planner", "Ad Copywriter"],
        icons=["briefcase", "globe", "key", "pencil"],
        default_index=0
    )

# Route to the selected module
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

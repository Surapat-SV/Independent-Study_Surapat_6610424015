# SEM Planner - Streamlit Application with AI Agents

# Import necessary libraries
import streamlit as st
import os
import json
import pandas as pd
import numpy as np
from crewai import Agent, Task, Crew
from langchain.vectorstores import FAISS
from langchain.embeddings.google import GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from google.cloud import bigquery

# Set environment variables for API keys
os.environ['GEMINI_API_KEY'] = st.secrets["GOOGLE_API_KEY"]

# Page Configuration
st.set_page_config(page_title="SEM Planner", layout="wide")

# Sidebar for navigation
st.sidebar.title("SEM Planner")
st.sidebar.subheader("Select Step:")
page = st.sidebar.radio("", ["Page 1", "Page 2", "Page 3", "Page 4", "Report"])

# Agent Setup
embedding_model = GoogleGenerativeAIEmbeddings()

# Query BigQuery
def query_bigquery(sql_query):
    """Query data from Google BigQuery."""
    client = bigquery.Client()
    query_job = client.query(sql_query)
    results = query_job.result()
    df = results.to_dataframe()
    return df

# Page 1: Business Understanding Agent
if page == "Page 1":
    st.title("Business Understanding Agent")
    st.write("Input: Provide Business Overview, Target Audience, Product/Service Details")

    # Inputs
    business_overview = st.text_area("Business Overview")
    target_audience = st.text_area("Target Audience")
    product_details = st.text_area("Product/Service Details")

    # Create Agent and Task
    business_agent = Agent(
        role="Business Analyst",
        goal="Understand business context and define target audience.",
        tools=[],
        verbose=True,
    )

    business_task = Task(
        description="Analyze business overview, target audience, and product details.",
        agent=business_agent
    )

    business_crew = Crew(agents=[business_agent], tasks=[business_task])

    if st.button("Process Business Data"):
        result = business_crew.kickoff(inputs={
            "overview": business_overview,
            "audience": target_audience,
            "product": product_details
        })
        st.write("Agent Output:", result)

# Page 2: Web Scraper Agent
elif page == "Page 2":
    st.title("Web Scraper Agent")
    st.write("Input: Website URLs (ours and competitors)")

    # Inputs
    our_url = st.text_input("Our Website URL")
    competitor_url = st.text_input("Competitor Website URL")

    # Create Agent and Task
    scraper_agent = Agent(
        role="Web Scraper",
        goal="Extract and compare metadata from websites.",
        tools=[],
        verbose=True,
    )

    scraper_task = Task(
        description="Scrape and compare metadata between URLs.",
        agent=scraper_agent
    )

    scraper_crew = Crew(agents=[scraper_agent], tasks=[scraper_task])

    if st.button("Scrape and Analyze"):
        result = scraper_crew.kickoff(inputs={
            "our_url": our_url,
            "competitor_url": competitor_url
        })
        st.write("Scraper Output:", result)

# Page 3: Keyword Planning Agent
elif page == "Page 3":
    st.title("Keyword Planning Agent")
    st.write("Input: Query from BigQuery based on user idea.")

    # Inputs
    user_query = st.text_area("Enter your query for keywords")

    # Create Agent and Task
    planning_agent = Agent(
        role="Keyword Planner",
        goal="Generate keyword recommendations based on BigQuery data.",
        tools=[],
        verbose=True,
    )

    planning_task = Task(
        description="Fetch keyword data from BigQuery.",
        agent=planning_agent
    )

    planning_crew = Crew(agents=[planning_agent], tasks=[planning_task])

    if st.button("Generate Keywords"):
        sql_query = f"""
        SELECT keyword, clicks, impressions
        FROM `project.dataset.adwords_data`
        WHERE keyword LIKE '%{user_query}%'
        """
        data = query_bigquery(sql_query)
        st.write("Query Results:")
        st.dataframe(data)

# Page 4: Ads Copywriter Agent
elif page == "Page 4":
    st.title("Ads Copywriter Agent")
    st.write("Input: Use data from previous agents.")

    # Inputs
    ad_headline = st.text_input("Ad Headline (30 characters)")
    ad_description = st.text_area("Ad Description (90 characters)")

    # Create Agent and Task
    copywriter_agent = Agent(
        role="Ads Copywriter",
        goal="Generate ad headlines and descriptions.",
        tools=[],
        verbose=True,
    )

    copywriter_task = Task(
        description="Generate ad copy for SEM campaigns.",
        agent=copywriter_agent
    )

    copywriter_crew = Crew(agents=[copywriter_agent], tasks=[copywriter_task])

    if st.button("Generate Ads Copy"):
        result = copywriter_crew.kickoff(inputs={
            "headline": ad_headline,
            "description": ad_description
        })
        st.write("Generated Ad Copy:")
        st.write(result)

# Page 5: Project Manager Agent
elif page == "Report":
    st.title("SEM Planning Report")
    st.write("Combining information into a comprehensive SEM report.")

    # Simulate Report Generation
    st.markdown("## Final SEM Report")
    st.markdown("### Business Overview")
    st.markdown("[Business Overview Data Here]")
    st.markdown("### Target Audience")
    st.markdown("[Target Audience Data Here]")
    st.markdown("### Keyword Analysis")
    st.markdown("Keywords comparison results displayed here.")
    st.markdown("### Ads Copy")
    st.markdown("Headline: [Generated Headline Here]")
    st.markdown("Description: [Generated Description Here]")

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

# Helper Function: Create FAISS Index
def create_faiss_index(documents, embedding_model):
    """Create a FAISS index for storing embeddings."""
    index = FAISS.from_documents(documents, embedding_model)
    return index

# Define Dummy Data for Testing
dummy_data = [
    {"content": "This is a test document about SEM strategies."},
    {"content": "Keyword planning for Google Ads optimization."},
]

# Create FAISS Index
docs = [PromptTemplate(input_variables=[], template=d['content']) for d in dummy_data]
faiss_index = create_faiss_index(docs, embedding_model)

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

    # Create Agent
    business_agent = Agent(
        role="Business Analyst",
        goal="Understand business context and define target audience.",
        tools=[],
        verbose=True,
    )

    if st.button("Process Business Data"):
        result = business_agent.run(f"Overview: {business_overview}, Audience: {target_audience}, Product: {product_details}")
        st.write("Agent Output:", result)

# Page 2: Web Scraper Agent
elif page == "Page 2":
    st.title("Web Scraper Agent")
    st.write("Input: Website URLs (ours and competitors)")

    # Inputs
    our_url = st.text_input("Our Website URL")
    competitor_url = st.text_input("Competitor Website URL")

    if st.button("Scrape and Analyze"):
        # Simulate scraping and keyword analysis
        st.write(f"Scraping data from {our_url} and {competitor_url}")
        st.write("Comparison Results: Keywords matched and differences identified.")

# Page 3: Keyword Planning Agent
elif page == "Page 3":
    st.title("Keyword Planning Agent")
    st.write("Input: Query from BigQuery based on user idea.")

    # Inputs
    user_query = st.text_area("Enter your query for keywords")

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

    if st.button("Generate Ads Copy"):
        st.write("Generated Ad Copy:")
        st.write(f"Headline: {ad_headline}")
        st.write(f"Description: {ad_description}")

# Page 5: Project Manager Agent
elif page == "Report":
    st.title("SEM Planning Report")
    st.write("Combining information into a comprehensive SEM report.")

    # Simulate Report Generation
    st.markdown("## Final SEM Report")
    st.markdown("### Business Overview")
    st.markdown(business_overview)
    st.markdown("### Target Audience")
    st.markdown(target_audience)
    st.markdown("### Keyword Analysis")
    st.markdown("Keywords comparison results displayed here.")
    st.markdown("### Ads Copy")
    st.markdown(f"Headline: {ad_headline}")
    st.markdown(f"Description: {ad_description}")

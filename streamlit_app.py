import streamlit as st
from crewai import Agent, Task, Crew
import json
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from google.cloud import bigquery
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

# Page Configuration
st.set_page_config(page_title="SEM Planner", layout="wide")

# Sidebar Navigation
pages = ["Page 1", "Page 2", "Page 3", "Page 4", "PM Report"]
page = st.sidebar.radio("Select Step:", pages)

# Shared Memory for storing outputs (using session state)
if "memory" not in st.session_state:
    st.session_state.memory = {}

if "web_data" not in st.session_state:
    st.session_state.web_data = {}

if "keyword_data" not in st.session_state:
    st.session_state.keyword_data = {}

# --------------------------------------------
# Page 1: Business Understanding Agent
if page == "Page 1":
    st.title("Business Understanding Agent")

    # Inputs for Business Overview
    business_overview = st.text_area("Enter Business Overview:")
    target_audience = st.text_area("Define Target Audience:")
    product_details = st.text_area("Describe Product/Service:")

    if st.button("Store Information"):
        # Store data as JSON
        st.session_state.memory['business'] = {
            'overview': business_overview,
            'audience': target_audience,
            'product': product_details
        }
        st.success("Business Information Stored Successfully!")

    # Display stored information
    if 'business' in st.session_state.memory:
        st.json(st.session_state.memory['business'])


# --------------------------------------------
# Page 2: Web Scraper Agent
if page == "Page 2":
    st.title("Web Scraper Agent")

    # Inputs for URLs
    our_url = st.text_input("Our Website URL:")
    competitor_url = st.text_input("Competitor's Website URL:")

    if st.button("Scrape and Compare"):
        # Scraping function
        def scrape_meta_tags(url):
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                meta_tags = {tag.get('name', '').lower(): tag.get('content', '') for tag in soup.find_all('meta')}
                return meta_tags
            except Exception as e:
                return str(e)

        # Store scraped data
        our_data = scrape_meta_tags(our_url)
        competitor_data = scrape_meta_tags(competitor_url)

        st.session_state.web_data['our'] = our_data
        st.session_state.web_data['competitor'] = competitor_data

        # Display results
        st.subheader("Our Website Meta Tags")
        st.json(our_data)

        st.subheader("Competitor's Website Meta Tags")
        st.json(competitor_data)

    # Keyword Comparison
    if st.button("Compare Keywords"):
        our_keywords = set(st.session_state.web_data['our'].values())
        competitor_keywords = set(st.session_state.web_data['competitor'].values())

        common_keywords = our_keywords & competitor_keywords
        diff_keywords = our_keywords - competitor_keywords

        st.write("Common Keywords:", common_keywords)
        st.write("Unique Keywords:", diff_keywords)


# --------------------------------------------
# Page 3: Keyword Planning Agent
if page == "Page 3":
    st.title("Keyword Planning Agent")

    # Inputs for user idea
    user_idea = st.text_input("Enter Idea for Keywords:")

    if st.button("Fetch Keywords"):
        # Connect to BigQuery and query based on user idea
        client = bigquery.Client()
        query = f"""
        SELECT keyword, search_volume
        FROM `project.dataset.keyword_table`
        WHERE keyword LIKE '%{user_idea}%'
        ORDER BY search_volume DESC
        LIMIT 10
        """
        results = client.query(query).to_dataframe()
        st.session_state.keyword_data = results

        # Display Results
        st.dataframe(results)


# --------------------------------------------
# Page 4: Ads Copywriter Agent
if page == "Page 4":
    st.title("Ads Copywriter Agent")

    # Generate Ads based on previous data
    if st.button("Generate Ads"):
        business = st.session_state.memory.get('business', {})
        keywords = st.session_state.keyword_data

        headlines = [f"{keyword} - {business.get('product', '')}" for keyword in keywords['keyword'][:3]]
        descriptions = [f"Find out about {business.get('product', '')} for {keyword}." for keyword in keywords['keyword'][:3]]

        # Display ads
        for i in range(len(headlines)):
            st.write(f"**Headline {i+1}:** {headlines[i]}")
            st.write(f"**Description {i+1}:** {descriptions[i]}")


# --------------------------------------------
# PM Agent - Final Report
if page == "PM Report":
    st.title("SEM Planning Report")

    # Combine all information
    report = """
    <h2>SEM Planning Report</h2>
    <h3>Business Understanding</h3>
    <p>{}</p>
    <h3>Web Analysis</h3>
    <p>Our Meta Tags: {}</p>
    <p>Competitor Meta Tags: {}</p>
    <h3>Keyword Plan</h3>
    <p>{}</p>
    <h3>Ad Copy</h3>
    <p>{}</p>
    """.format(
        json.dumps(st.session_state.memory.get('business', {})),
        json.dumps(st.session_state.web_data.get('our', {})),
        json.dumps(st.session_state.web_data.get('competitor', {})),
        st.session_state.keyword_data.to_json() if 'keyword_data' in st.session_state else "No data",
        "Ad Templates Available in Page 4"
    )
    
    st.markdown(report, unsafe_allow_html=True)

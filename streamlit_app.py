import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from google.generativeai import GenerativeModel, configure
import json

# Capture Gemini API Key
gemini_api_key = st.text_input("Gemini API Key:", placeholder="Type your API Key here...", type="password")

# Configure Gemini API
if gemini_api_key:
    configure(api_key=gemini_api_key)
    model = GenerativeModel("gemini-1.5-pro")

# Streamlit Setup
st.title("SEM Planner")
st.sidebar.title("Select Step:")
page = st.sidebar.radio("", ["Business Understanding Agent", "Web Scraper Agent - SEM Planner", "Keyword Planner", "Ads generation"])

# Initialize Session State for Business Understanding Agent
if "business_overview" not in st.session_state:
    st.session_state.business_overview = ""
if "target_audience" not in st.session_state:
    st.session_state.target_audience = ""
if "product_details" not in st.session_state:
    st.session_state.product_details = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------- PAGE 1: BUSINESS UNDERSTANDING AGENT --------------------
if page == "Business Understanding Agent":
    st.subheader("Business Understanding Chatbot")

    # Display chat history
    for role, message in st.session_state.chat_history:
        st.chat_message(role).markdown(message)

    # Input user message
    user_input = st.chat_input("Tell me about your business or ask any questions.")

    if user_input:
        # Display user message
        st.session_state.chat_history.append(("user", user_input))
        st.chat_message("user").markdown(user_input)

        # Create prompt for Gemini to analyze and extract business details
        prompt = f"""
        You are an assistant that helps users define their business information for SEM planning.
        Based on the following user input, extract details about:
        1. Business Overview
        2. Target Audience
        3. Product/Service Details

        User Input: {user_input}

        If the details are incomplete, ask follow-up questions to clarify the requirements.
        Provide only the extracted or clarified information as structured output.
        """

        # Generate Gemini response
        response = model.generate_content(prompt)
        bot_response = response.text if response else "I couldn't process that, please try again."

        # Display Gemini's response
        st.session_state.chat_history.append(("assistant", bot_response))
        st.chat_message("assistant").markdown(bot_response)

        # Extract structured data from Gemini response (mock example, update later)
        try:
            parsed_response = json.loads(bot_response)
            st.session_state.business_overview = parsed_response.get("Business Overview", "")
            st.session_state.target_audience = parsed_response.get("Target Audience", "")
            st.session_state.product_details = parsed_response.get("Product/Service Details", "")
        except Exception as e:
            st.warning("Failed to parse structured data. Please clarify the information.")

    # Show extracted information
    st.subheader("Extracted Information")
    st.json({
        "Business Overview": st.session_state.business_overview,
        "Target Audience": st.session_state.target_audience,
        "Product/Service Details": st.session_state.product_details
    })

# -------------------- PAGE 2: WEB SCRAPER AGENT --------------------
elif page == "Web Scraper Agent - SEM Planner":
    st.subheader("Compare Keywords and Generate SEM Checklist")

    # Input URLs
    our_url = st.text_input("Our Website URL")
    competitor_url = st.text_input("Competitor Website URL")

    @st.cache_data
    def fetch_html(url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return BeautifulSoup(response.text, 'html.parser')
            else:
                st.error(f"Failed to fetch {url}. Status code: {response.status_code}")
                return None
        except Exception as e:
            st.error(f"Error fetching {url}: {e}")
            return None

    # Function: Extract Meta Tags
    def extract_meta_data(soup):
        title = soup.title.string if soup.title else "No Title"
        description = ""
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc:
            description = meta_desc.get("content", "")
        return title, description

    # Analyze websites
    if st.button("Analyze Websites"):
        if our_url and competitor_url:
            our_soup = fetch_html(our_url)
            competitor_soup = fetch_html(competitor_url)
            if our_soup and competitor_soup:
                our_meta = extract_meta_data(our_soup)
                comp_meta = extract_meta_data(competitor_soup)
                st.write(f"**Our Title:** {our_meta[0]}")
                st.write(f"**Competitor Title:** {comp_meta[0]}")
        else:
            st.warning("Please enter both URLs to proceed.")

# -------------------- PAGE 3: KEYWORD PLANNER --------------------
elif page == "Keyword Planner":
    st.subheader("Keyword Planner - Coming Soon")

# -------------------- PAGE 4: ADS GENERATION --------------------
elif page == "Ads generation":
    st.subheader("Ads Generation - Coming Soon")

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
import json

# Capture Gemini API Key
gemini_api_key = st.text_input("Gemini API Key:", placeholder="Type your API Key here...", type="password")

# Configure Gemini API
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-1.5-pro")

# Streamlit Setup
st.title("SEM Planner")
st.sidebar.title("Select Step:")
page = st.sidebar.radio("", ["Business Understanding Agent", "Web Scraper Agent - SEM Planner", "Keyword Planner", "Ads Generation"])

# Session State for Business Details
if 'business_data' not in st.session_state:
    st.session_state.business_data = {
        "Business Overview": "",
        "Target Audience": "",
        "Product/Service Details": ""
    }

if page == "Business Understanding Agent":
    st.subheader("Business Understanding Agent - Chatbot")

    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for role, message in st.session_state.chat_history:
        st.chat_message(role).markdown(message)

    # Chat input for conversation
    user_input = st.chat_input("Tell me about your business or target audience...")

    # Process input if provided
    if user_input:
        # Append user input to chat history
        st.session_state.chat_history.append(("user", user_input))
        st.chat_message("user").markdown(user_input)

        # Use Gemini to help define the target audience
        if gemini_api_key:
            prompt = (
                f"Analyze this input and extract details about the business overview, target audience, and product/service details: {user_input}. "
                "Provide a summary focusing on defining the target audience based on the input provided."
            )
            try:
                response = model.generate_content(prompt)
                gemini_response = response.text

                # Append Gemini's response to chat history
                st.session_state.chat_history.append(("assistant", gemini_response))
                st.chat_message("assistant").markdown(gemini_response)

                # Extract business data using Gemini's response
                st.session_state.business_data["Business Overview"] = user_input
                st.session_state.business_data["Target Audience"] = gemini_response
                st.session_state.business_data["Product/Service Details"] = user_input

            except Exception as e:
                st.error(f"An error occurred while using Gemini: {e}")

    # Display saved details
    st.subheader("Saved Information")
    st.json(st.session_state.business_data)

elif page == "Web Scraper Agent - SEM Planner":
    st.subheader("Compare Keywords and Generate SEM Checklist")

    # Input URLs
    our_url = st.text_input("Our Website URL")
    competitor_url = st.text_input("Competitor Website URL")

    # Function: Fetch and Parse HTML
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

    # Function: Extract Keywords
    def extract_keywords(soup):
        texts = soup.get_text().lower()
        words = pd.Series(texts.split())
        stopwords = set(["the", "is", "and", "to", "in", "of", "a", "on", "with", "for", "this", "that", "it", "as"])
        keywords = words[~words.isin(stopwords)].value_counts().head(20)
        return keywords

    # Function: Compute Cosine Similarity
    def compute_similarity(our_text, competitor_text):
        vectorizer = CountVectorizer().fit_transform([our_text, competitor_text])
        vectors = vectorizer.toarray()
        similarity = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
        return similarity

    # Process URLs
    if st.button("Analyze Websites"):
        if our_url and competitor_url:
            # Fetch HTML
            our_soup = fetch_html(our_url)
            competitor_soup = fetch_html(competitor_url)

            if our_soup and competitor_soup:
                # Extract Metadata
                our_meta = extract_meta_data(our_soup)
                comp_meta = extract_meta_data(competitor_soup)

                # Extract Keywords
                our_keywords = extract_keywords(our_soup)
                comp_keywords = extract_keywords(competitor_soup)

                # Compute Similarity
                similarity = compute_similarity(' '.join(our_keywords.index), ' '.join(comp_keywords.index))

                # Display Results
                st.subheader("Metadata Analysis")
                st.write(f"**Our Title:** {our_meta[0]}")
                st.write(f"**Our Description:** {our_meta[1]}")
                st.write(f"**Competitor Title:** {comp_meta[0]}")
                st.write(f"**Competitor Description:** {comp_meta[1]}")

                st.subheader("Keyword Analysis")
                st.write("**Our Top Keywords:")
                st.write(our_keywords)
                st.write("**Competitor Top Keywords:")
                st.write(comp_keywords)

                st.subheader("Comparison Results")
                st.write(f"**Keyword Similarity (Cosine):** {similarity:.2f}")
            else:
                st.error("Failed to fetch HTML content from one or both URLs.")
        else:
            st.warning("Please enter both URLs to proceed.")

elif page == "Keyword Planner":
    st.subheader("Keyword Planner - Coming Soon")

elif page == "Ads Generation":
    st.subheader("Ads Generation - Coming Soon")

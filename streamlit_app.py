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

# Initialize session state for business details and chat history
if 'business_data' not in st.session_state:
    st.session_state.business_data = {
        "Business Name": "",
        "Product/Service": "",
        "Location": "",
        "Necessary Information": "",
        "Target Audience": ""
    }

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'question_index' not in st.session_state:
    st.session_state.question_index = 0

# List of predefined questions
questions = [
    "What is your business name?",
    "What products or services do you offer?",
    "Do you have any physical stores? If yes, where are they located?",
    "Please provide any other necessary information about your business."
]

# Display chat history
st.subheader("Business Understanding Agent - Chatbot")
for role, message in st.session_state.chat_history:
    st.chat_message(role).markdown(message)

# Greeting message if the chat starts
if st.session_state.question_index == 0:
    greeting = "Hello! My name is N'Assist, your new intern. I'll help you define your target audience."
    st.session_state.chat_history.append(("assistant", greeting))
    st.chat_message("assistant").markdown(greeting)

# Ask the current question
if st.session_state.question_index < len(questions):
    current_question = questions[st.session_state.question_index]
    st.session_state.chat_history.append(("assistant", current_question))
    st.chat_message("assistant").markdown(current_question)

    # Chat input for user response
    user_input = st.chat_input("Your response...")
    if user_input:
        # Save user input and progress to the next question
        st.session_state.chat_history.append(("user", user_input))
        st.chat_message("user").markdown(user_input)

        # Save responses based on the question index
        if st.session_state.question_index == 0:
            st.session_state.business_data["Business Name"] = user_input
        elif st.session_state.question_index == 1:
            st.session_state.business_data["Product/Service"] = user_input
        elif st.session_state.question_index == 2:
            st.session_state.business_data["Location"] = user_input
        elif st.session_state.question_index == 3:
            st.session_state.business_data["Necessary Information"] = user_input

        # Move to the next question
        st.session_state.question_index += 1

# Final summary after all questions
if st.session_state.question_index == len(questions):
    summary_message = (
        "Thank you for providing the details! Here's the summary of your business information:"
    )
    st.session_state.chat_history.append(("assistant", summary_message))
    st.chat_message("assistant").markdown(summary_message)

    # Extract details about target audience using Gemini (if API key is provided)
    if gemini_api_key:
        prompt = (
            f"Based on the following details, define the target audience:\n"
            f"Business Name: {st.session_state.business_data['Business Name']}\n"
            f"Product/Service: {st.session_state.business_data['Product/Service']}\n"
            f"Location: {st.session_state.business_data['Location']}\n"
            f"Necessary Information: {st.session_state.business_data['Necessary Information']}"
        )
        try:
            response = model.generate_content(prompt)
            gemini_response = response.text
            st.session_state.business_data["Target Audience"] = gemini_response
            st.session_state.chat_history.append(("assistant", gemini_response))
            st.chat_message("assistant").markdown(gemini_response)
        except Exception as e:
            st.error(f"An error occurred while using Gemini: {e}")

    # Display the saved business information
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

    # Gemini Analysis for SEM Checklist
    def analyze_with_gemini(our_meta, comp_meta, our_keywords, comp_keywords):
        prompt = f"""
        Analyze and compare the following website metadata and keywords for SEM planning:
        Our Website:
        Title: {our_meta[0]}
        Description: {our_meta[1]}
        Keywords: {', '.join(our_keywords.index)}

        Competitor Website:
        Title: {comp_meta[0]}
        Description: {comp_meta[1]}
        Keywords: {', '.join(comp_keywords.index)}

        Provide insights, recommendations, and identify gaps to improve SEM strategies.
        """
        response = model.generate_content(prompt)
        return response.text

    # Process URLs
    if st.button("Analyze Websites"):
        if our_url and competitor_url:
            our_soup = fetch_html(our_url)
            competitor_soup = fetch_html(competitor_url)

            if our_soup and competitor_soup:
                our_meta = extract_meta_data(our_soup)
                comp_meta = extract_meta_data(competitor_soup)
                our_keywords = extract_keywords(our_soup)
                comp_keywords = extract_keywords(competitor_soup)
                similarity = compute_similarity(' '.join(our_keywords.index), ' '.join(comp_keywords.index))
                gemini_analysis = analyze_with_gemini(our_meta, comp_meta, our_keywords, comp_keywords)

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

                st.subheader("Gemini Analysis Recommendations")
                st.write(gemini_analysis)
            else:
                st.error("Failed to fetch HTML content from one or both URLs.")
        else:
            st.warning("Please enter both URLs to proceed.")

elif page == "Keyword Planner":
    st.subheader("Keyword Planner - Coming Soon")

elif page == "Ads Generation":
    st.subheader("Ads Generation - Coming Soon")

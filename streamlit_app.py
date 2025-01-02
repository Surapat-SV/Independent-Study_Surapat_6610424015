import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
import json
import matplotlib.pyplot as plt
from pythainlp import word_tokenize
from pythainlp.corpus.common import thai_stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

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

if page == "Business Understanding Agent":
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

    # Function: Extract and preprocess keywords using PyThaiNLP
    def extract_keywords_with_pythainlp(soup):
        texts = soup.get_text().lower()
        tokens = word_tokenize(texts)
        stopwords = set(thai_stopwords())
        filtered_tokens = [word for word in tokens if word not in stopwords and len(word) > 1]
        return filtered_tokens

    # Function: Compute TF-IDF
    def compute_tfidf(our_tokens, comp_tokens):
        corpus = [' '.join(our_tokens), ' '.join(comp_tokens)]
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(corpus)
        feature_names = vectorizer.get_feature_names_out()
        return tfidf_matrix, feature_names

    # Function: Generate Gemini Analysis and Plot Graph
    def gemini_analyze_and_plot(our_keywords, comp_keywords, tfidf_matrix, feature_names):
        prompt = f"""
        Compare the following keyword distributions for SEM planning:
        Our Website Keywords: {', '.join(our_keywords[:20])}
        Competitor Website Keywords: {', '.join(comp_keywords[:20])}
        
        Provide insights, recommendations, and visualize the keyword distribution differences.
        """
        try:
            response = model.generate_content(prompt)
            gemini_response = response.text
        except Exception as e:
            st.error(f"Gemini API Error: {e}")
            return None

        # Generate a plot for keyword distribution
        tfidf_scores = tfidf_matrix.toarray()
        our_scores = tfidf_scores[0]
        comp_scores = tfidf_scores[1]
        
        plt.figure(figsize=(10, 6))
        indices = np.arange(len(feature_names))
        width = 0.35
        plt.bar(indices, our_scores, width, label="Our Website")
        plt.bar(indices + width, comp_scores, width, label="Competitor Website")
        plt.xlabel("Keywords")
        plt.ylabel("TF-IDF Score")
        plt.title("Keyword Distribution Comparison")
        plt.xticks(indices + width / 2, feature_names, rotation=90)
        plt.legend()
        st.pyplot(plt)

        return gemini_response

    # Function: Compute Cosine Similarity
    def compute_cosine_similarity(tfidf_matrix):
        # Compute cosine similarity between two vectors
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return cosine_sim

    # Function: Interpret Similarity Using Gemini
    def interpret_similarity_with_gemini(similarity):
        prompt = f"""
        Analyze the following cosine similarity value ({similarity:.2f}) between two sets of keywords.
        Provide an interpretation of whether this value indicates high, medium, or low similarity and what this means in the context of SEM (Search Engine Marketing).
        """
        try:
            response = model.generate_content(prompt)
            interpretation = response.text
        except Exception as e:
            st.error(f"Gemini API Error: {e}")
            return "Error occurred while interpreting similarity."
        return interpretation

    # Process URLs
    if st.button("Analyze Websites"):
        if our_url and competitor_url:
            our_soup = fetch_html(our_url)
            competitor_soup = fetch_html(competitor_url)

            if our_soup and competitor_soup:
                # Extract and preprocess keywords
                our_tokens = extract_keywords_with_pythainlp(our_soup)
                comp_tokens = extract_keywords_with_pythainlp(competitor_soup)

                # Compute TF-IDF
                tfidf_matrix, feature_names = compute_tfidf(our_tokens, comp_tokens)

                # Compute Cosine Similarity
                cosine_sim = compute_cosine_similarity(tfidf_matrix)

                # Interpret similarity using Gemini
                similarity_interpretation = interpret_similarity_with_gemini(cosine_sim)

                # Gemini Analysis and Plot
                gemini_analysis = gemini_analyze_and_plot(our_tokens, comp_tokens, tfidf_matrix, feature_names)

                # Display results
                st.subheader("Cosine Similarity")
                st.write(f"**Cosine Similarity Score:** {cosine_sim:.2f}")
                st.write(f"**Gemini Interpretation:** {similarity_interpretation}")

                if gemini_analysis:
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

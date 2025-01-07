__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from crewai import Crew
from agents.website_analyst_agents import WebsiteAnalystAgents
from tasks.website_analyst_tasks import WebsiteAnalystTasks
import datetime
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pythainlp.tokenize import word_tokenize
from pythainlp.corpus.common import thai_stopwords
import string
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Cache data for HTML fetching
@st.cache_data
def fetch_html(url):
    """
    Fetches HTML content from the specified URL.
    """
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


# Extract and preprocess keywords using Thai NLP
def extract_keywords_with_pythainlp(soup):
    """
    Extracts and preprocesses keywords using Thai NLP tools.
    """
    text = soup.get_text().lower()
    tokens = word_tokenize(text)
    stopwords = set(thai_stopwords())
    filtered_tokens = [word for word in tokens if word not in stopwords and len(word) > 1]
    return filtered_tokens


# Compute TF-IDF
def compute_tfidf(our_tokens, comp_tokens):
    """
    Computes TF-IDF scores for the given keywords.
    """
    corpus = [' '.join(our_tokens), ' '.join(comp_tokens)]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    feature_names = vectorizer.get_feature_names_out()
    return tfidf_matrix, feature_names


# Compute Cosine Similarity
def compute_cosine_similarity(tfidf_matrix):
    """
    Computes cosine similarity between two sets of keywords.
    """
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]


# Plot Top Keywords
def plot_top_keywords(tfidf_matrix, feature_names, top_n=5):
    """
    Plots the top keywords by TF-IDF scores for both websites.
    """
    tfidf_scores = tfidf_matrix.toarray()
    our_scores = tfidf_scores[0]
    comp_scores = tfidf_scores[1]

    top_our_indices = np.argsort(our_scores)[::-1][:top_n]
    top_comp_indices = np.argsort(comp_scores)[::-1][:top_n]

    top_our_keywords = [feature_names[i] for i in top_our_indices]
    top_comp_keywords = [feature_names[i] for i in top_comp_indices]
    top_our_values = our_scores[top_our_indices]
    top_comp_values = comp_scores[top_comp_indices]

    indices = np.arange(len(top_our_keywords))
    width = 0.35
    plt.bar(indices, top_our_values, width, label="Our Website")
    plt.bar(indices + width, top_comp_values, width, label="Competitor")
    plt.xlabel("Keywords")
    plt.ylabel("TF-IDF Score")
    plt.title(f"Top {top_n} Keyword Comparison")
    plt.xticks(indices + width / 2, top_our_keywords, rotation=45, ha="right")
    plt.legend()
    st.pyplot(plt)


# Render output based on format
def display_output(output):
    """
    Renders output as Markdown, HTML, or Plain Text based on content.
    """
    if isinstance(output, str):
        if output.startswith("###") or output.startswith("#"):
            st.markdown(output, unsafe_allow_html=True)
        else:
            st.write(output)
    elif isinstance(output, dict):
        for key, value in output.items():
            st.write(f"**{key}:** {value}")
    else:
        st.write(output)


# Run Web Analyst
def run_web_analyst():
    """
    Displays the Web Analyst interface for keyword and SEO analysis.
    """
    # UI Header
    st.header("Web Analyst")
    st.markdown("Analyze and compare your website against a competitor for SEO improvements.")

    # User Inputs
    our_url = st.text_input("Our Website URL:", placeholder="https://www.ourwebsite.com")
    competitor_url = st.text_input("Competitor Website URL:", placeholder="https://www.competitor.com")

    # Analyze Button
    if st.button("Analyze Websites"):
        if not our_url or not competitor_url:
            st.error("Please provide both URLs for analysis.")
            return

        try:
            # Fetch and process HTML content
            our_soup = fetch_html(our_url)
            comp_soup = fetch_html(competitor_url)

            if not our_soup or not comp_soup:
                st.error("Failed to fetch content from one or both websites.")
                return

            # Extract and preprocess keywords
            st.subheader("Keyword Extraction")
            our_keywords = extract_keywords_with_pythainlp(our_soup)
            comp_keywords = extract_keywords_with_pythainlp(comp_soup)

            st.markdown("**Sample Keywords - Our Website:**")
            st.write(", ".join(our_keywords[:20]))
            st.markdown("**Sample Keywords - Competitor Website:**")
            st.write(", ".join(comp_keywords[:20]))

            # TF-IDF and Cosine Similarity
            st.subheader("Keyword Analysis")
            tfidf_matrix, feature_names = compute_tfidf(our_keywords, comp_keywords)
            similarity = compute_cosine_similarity(tfidf_matrix)
            st.markdown(f"**Cosine Similarity Score:** `{similarity:.2f}`")

            # Plot Keyword Distribution
            st.subheader("Keyword Distribution")
            plot_top_keywords(tfidf_matrix, feature_names, top_n=5)

            # Agent Tasks and Execution
            st.subheader("Agent Execution")
            agents = WebsiteAnalystAgents()
            tasks = WebsiteAnalystTasks()
            agent = agents.web_analyst_agent()
            task1 = tasks.website_analysis_task(agent, our_url, competitor_url)
            task2 = tasks.keyword_similarity_task(agent, our_keywords, comp_keywords)

            crew = Crew(agents=[agent], tasks=[task1, task2], verbose=True)
            results = crew.kickoff()

            # Display Results
            st.subheader("Analysis Results")
            for i, result in enumerate(results):
                st.markdown(f"### Task {i + 1} Output")
                display_output(result)

            # Key Insights and Recommendations
            st.subheader("Key Insights")
            st.markdown("""
            - **Fill Keyword Gaps:** Optimize metadata with high-performing keywords.
            - **Improve SEO Tags:** Update descriptions and titles based on findings.
            - **Refine Ad Copy:** Target competitive keywords in SEM campaigns.
            """)

        except Exception as e:
            st.error(f"An error occurred during analysis: {str(e)}")

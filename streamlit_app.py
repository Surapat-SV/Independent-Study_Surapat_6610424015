import pandas as pd
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
from google.generativeai import GenerativeModel, configure

# Capture Gemini API Key
gemini_api_key = st.text_input("Gemini API Key:", placeholder="Type your API Key here...", type="password")

# Configure Gemini API
configure(api_key=gemini_api_key)
model = GenerativeModel("gemini-1.5-pro")

# Streamlit Setup
st.title("Web Scraper Agent - SEM Planner")
st.sidebar.title("Select Step:")
page = st.sidebar.radio("", ["Page 1", "Page 2", "Page 3", "Page 4"])

if page == "Page 2":
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

    # Function: Use Gemini for Analysis
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

                # Gemini Analysis
                gemini_analysis = analyze_with_gemini(our_meta, comp_meta, our_keywords, comp_keywords)

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

                if similarity > 0.7:
                    st.success("Your website keywords are highly similar to the competitor. Great job!")
                elif similarity > 0.4:
                    st.warning("Moderate similarity. Consider improving keyword alignment.")
                else:
                    st.error("Low similarity. Revise your keyword strategy.")

                st.subheader("Gemini Analysis Recommendations")
                st.write(gemini_analysis)
            else:
                st.error("Failed to fetch HTML content from one or both URLs.")
        else:
            st.warning("Please enter both URLs to proceed.")
else:
    st.write("Content on each page must be different.")

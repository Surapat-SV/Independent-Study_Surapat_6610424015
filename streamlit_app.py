# Import necessary libraries
import streamlit as st
import anthropic
import pandas as pd
import concurrent.futures
import base64
import json
import requests
from bs4 import BeautifulSoup
import openai
from pythainlp import word_tokenize

# Set up Streamlit app
st.set_page_config(page_title="Keyword Analysis and Ad Copy Generation", layout="wide")
st.title("Keyword Analysis and Ad Copy Generation")

# Sidebar for user inputs
with st.sidebar:
    st.subheader("User Inputs")
    
    # API key inputs
    anthropic_api_key = st.text_input("Enter your Anthropic API key:", type="password")
    openai_api_key = st.text_input("Enter your OpenAI API key:", type="password")
    gemini_api_key = st.text_input("Enter your Gemini API key:", type="password")
    openai = openai.Client(api_key=openai_api_key)

    # Keyword input
    input_type = st.radio("Select input type:", ("Manual", "CSV File"))
    if input_type == "Manual":
        default_keywords = """data destruction services
                              how to securely destroy digital data
                              data shredding companies near me"""
        keywords_input = st.text_area("Enter keywords (one per line):", value=default_keywords)
        keywords = [keyword.strip() for keyword in keywords_input.split("\n") if keyword.strip()]
    else:
        uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
        if uploaded_file is not None:
            keywords_df = pd.read_csv(uploaded_file)
            keywords = keywords_df['keyword'].tolist()
        else:
            keywords = []
    
    # Landing page URL input
    landing_page_url = st.text_input("Enter the landing page URL:", value="https://example.com")
    
    # Persona input for the ad writer
    persona = st.text_area("Define the persona for the ad writer:", value="Expert in high-CTR AdWords strategies.")
    
    # Additional parameters
    with st.expander("Advanced Settings"):
        max_retries = st.number_input("Max retries for ad copy generation", min_value=1, max_value=10, value=3)
        max_workers = st.number_input("Max concurrent workers", min_value=1, max_value=10, value=5)
        temperature = st.slider("Temperature for keyword analysis", min_value=0.0, max_value=1.0, value=0.2, step=0.1)
        ad_copy_temperature = st.slider("Temperature for ad copy generation", min_value=0.0, max_value=1.0, value=0.01, step=0.01)
        num_ads = st.number_input("Number of ad copies to generate", min_value=1, max_value=10, value=5)
    
    # Model selection for Anthropic
    model_options = {
        "Claude (Opus)": "claude-3-opus-20240229",
        "Claude (Sonnet)": "claude-3-sonnet-20240229",
        "Claude (Haiku)": "claude-3-haiku-20240307"
    }
    selected_model = st.selectbox("Select the Claude model:", list(model_options.keys()))
    
    # Start button
    start_button = st.button("Start Keyword Analysis")

# Main content area
col1, col2 = st.columns(2)

# Display landing page evaluation and progress
with col1:
    st.subheader("Landing Page Evaluation")
    if "landing_page_evaluation" not in st.session_state:
        st.session_state.landing_page_evaluation = ""
    st.write(st.session_state.landing_page_evaluation)

with col2:
    st.subheader("Progress")
    if "progress_text" not in st.session_state:
        st.session_state.progress_text = ""
    st.write(st.session_state.progress_text)

# Preprocess Thai keywords function
def preprocess_thai_keywords(keyword):
    return word_tokenize(keyword, engine='newmm')

# Function to get keyword analysis results
def get_keyword_analysis_results(keyword, persona):
    # Preprocess the keyword for Thai language support
    preprocessed_keyword = preprocess_thai_keywords(keyword)
    
    prompt = f"""
    You Are: {persona}. Analyze the following keyword for Google Ads campaigns:
    Keyword: {preprocessed_keyword}
    Instructions: 
    - Relevance, intent, buyer's journey stage, psychographics, demographics, CPC, search volume, competition level, quality score, and ad match type.
    Provide the results in JSON format.
    """
    
    try:
        # Call Anthropic API with the prompt
        result = anthropic.Anthropic(api_key=anthropic_api_key).messages.create(
            model=model_options[selected_model],
            system="Provide JSON only.",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000,
            temperature=temperature,
        )
        keyword_insights = json.loads(result.content[0].text.strip())
        return keyword_insights
    except Exception as e:
        # Error handling and using OpenAI to fix JSON
        gpt4_prompt = [{"role": "user", "content": f"Format this as JSON: {result.content[0].text.strip()}"}]
        gpt4_response = openai.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=gpt4_prompt,
            max_tokens=2000,
            temperature=0.2,
        )
        json_output = gpt4_response.choices[0].message.content.strip()
        try:
            keyword_insights = json.loads(json_output)
            return keyword_insights
        except Exception as e:
            return {"error": f"Failed to parse JSON: {str(e)}"}

# Function to get ad copies
def get_keyword_ad_copies(keyword, keyword_insights, landing_page_evaluation, persona):
    prompt = f"""
    Persona: {persona}. Generate {num_ads} expert-level ad copies for:
    Keyword: {keyword}
    Insights: {json.dumps(keyword_insights)}
    Landing Page: {landing_page_evaluation}
    Each ad should include headline1, headline2, headline3, description1, description2, path1, path2.
    """
    
    try:
        result = anthropic.Anthropic(api_key=anthropic_api_key).messages.create(
            model=model_options[selected_model],
            system="Expert at ad copywriting.",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000,
            temperature=ad_copy_temperature,
        )
        ad_copies = json.loads(result.content[0].text.strip())
        return ad_copies
    except Exception as e:
        # Error handling with OpenAI for JSON correction
        gpt4_prompt = [{"role": "user", "content": f"Format as JSON: {result.content[0].text.strip()}"}]
        gpt4_response = openai.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=gpt4_prompt,
            max_tokens=4000,
            temperature=0.2,
        )
        json_output = gpt4_response.choices[0].message.content.strip()
        try:
            return json.loads(json_output)
        except Exception as e:
            return [{"error": f"Failed to parse ad copies: {str(e)}"}]

# Function to evaluate landing page content
def evaluate_landing_page(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else ""
        description = soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else ""
        headings = " ".join([h.text for h in soup.find_all(['h1', 'h2', 'h3'])])
        paragraphs = " ".join([p.text for p in soup.find_all('p')])

        prompt = f"""
        Evaluate the landing page content for Google Ads:
        URL: {url}
        Title: {title}
        Description: {description}
        Headings: {headings}
        Paragraphs: {paragraphs}
        """
        
        result = anthropic.Anthropic(api_key=anthropic_api_key).messages.create(
            model=model_options[selected_model],
            system="Expert in evaluating landing pages.",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.5,
        )
        return result.content[0].text.strip()
    except Exception as e:
        return f"Error evaluating landing page: {str(e)}"

# Function to process a single keyword
def process_keyword(keyword, landing_page_evaluation, persona):
    keyword_insights = get_keyword_analysis_results(keyword, persona)
    st.session_state.progress_text = f"Analyzing keyword: {keyword}"
    ad_copies = get_keyword_ad_copies(keyword, keyword_insights, landing_page_evaluation, persona)
    return {
        "keyword": keyword,
        "insights": json.dumps(keyword_insights),
        "ad_copies": json.dumps(ad_copies)
    }

# Function to process keywords in parallel
def process_keywords(keywords, landing_page_evaluation, persona):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_keyword, kw, landing_page_evaluation, persona) for kw in keywords]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    return results

# Start analysis when the button is clicked
if start_button and anthropic_api_key and keywords and landing_page_url:
    with st.spinner("Evaluating landing page content..."):
        landing_page_evaluation = evaluate_landing_page(landing_page_url)
    st.session_state.landing_page_evaluation = landing_page_evaluation
    
    with st.spinner("Processing keywords..."):
        results = process_keywords(keywords, landing_page_evaluation, persona)
    
    st.session_state.progress_text = f"Processed {len(keywords)} keywords"
    st.success("Keyword processing completed!")
    
    # Convert results to DataFrame and display
    df = pd.DataFrame(results)
    st.subheader("Keyword Analysis Results")
    st.dataframe(df)

    # Download button for the results (CSV)
    csv_data = df.to_csv(index=False)
    b64 = base64.b64encode(csv_data.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="keyword_analysis_results.csv">Download CSV</a>'
    st.markdown(href, unsafe_allow_html=True)
else:
    st.warning("Provide the API key, keywords, and landing page URL, then click 'Start'.")

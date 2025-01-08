###############################################
# Website Analyst Tasks
# File: tasks/task_02_website_analyst.py
# Purpose: Defines tasks for website analysis and keyword optimization
###############################################

# Import required libraries
from crewai import Task  # Core CrewAI framework for tasks
from textwrap import dedent  # For multi-line string formatting
from crewai_tools import SerperDevTool, ScrapeWebsiteTool  # Tools for web search and scraping

# Class: Website Analyst Tasks
class WebsiteAnalystTasks:

    def website_analysis_task(self, agent, our_url, competitor_url):
        """
        Task: Analyze and compare metadata and keywords from two websites.
        Purpose: Identify SEM gaps, keyword opportunities, and optimization strategies.
        """
        return Task(
            description=dedent(f"""
                Perform metadata and keyword analysis to compare two websites.
                Identify SEO optimization opportunities and gaps.

                URLs:
                - Our Website: {our_url}
                - Competitor Website: {competitor_url}

                Deliverables:
                1. Extract metadata (titles, descriptions).
                2. Preprocess and tokenize keywords.
                3. Highlight keyword gaps and opportunities.

                Tools Used:
                - Web scraping for metadata.
                - Keyword extraction and analysis.
            """),
            expected_output="Markdown summary of metadata, keyword comparisons, and SEM insights.",
            agent=agent
        )

    def keyword_similarity_task(self, agent, our_keywords, competitor_keywords):
        """
        Task: Compare keyword similarities using TF-IDF and cosine similarity.
        Purpose: Evaluate keyword overlaps, gaps, and optimization opportunities.
        """
        return Task(
            description=dedent(f"""
                Analyze keyword similarity between two sets of keywords.
                Provide scores and insights into overlaps and gaps.

                Keywords:
                - Our Keywords: {', '.join(our_keywords)}
                - Competitor Keywords: {', '.join(competitor_keywords)}

                Deliverables:
                1. TF-IDF scores and cosine similarity metrics.
                2. Categorize similarity as Low, Medium, or High.
                3. Recommendations for keyword optimization.

                Tools Used:
                - TF-IDF vectorizer.
                - Cosine similarity computation.
            """),
            expected_output="Plain text summary of similarity scores and keyword recommendations.",
            agent=agent
        )

    def keyword_visualization_task(self, agent, tfidf_matrix, feature_names, top_n=5):
        """
        Task: Generate visualizations for keyword distribution based on TF-IDF scores.
        Purpose: Highlight keyword differences and optimization opportunities.
        """
        return Task(
            description=dedent(f"""
                Generate visualizations for keyword distribution using TF-IDF scores.
                Highlight the top {top_n} keywords for both websites.

                Deliverables:
                1. Visual plots comparing keyword distributions.
                2. Insights into keyword differences and optimization strategies.

                Tools Used:
                - TF-IDF analysis for keyword weighting.
                - Visualization libraries for graphical outputs.
            """),
            expected_output=f"Graphical visualizations of top {top_n} keywords with insights.",
            agent=agent
        )

# End of file: tasks/task_02_website_analyst.py

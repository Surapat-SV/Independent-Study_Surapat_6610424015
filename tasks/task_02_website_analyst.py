from crewai import Task
from textwrap import dedent
from datetime import date


class WebsiteAnalystTasks:

    def website_analysis_task(self, agent, our_url, competitor_url):
        return Task(
            description=dedent(f"""
                Analyze and compare metadata and keywords from two websites.
                Highlight SEM gaps, keyword opportunities, and optimization strategies.

                URLs:
                - Our Website: {our_url}
                - Competitor Website: {competitor_url}

                Deliverables:
                1. Extract metadata (titles and descriptions).
                2. Preprocess and tokenize keywords.
                3. Highlight keyword gaps and opportunities.

                Expected Output:
                - Metadata details (titles, descriptions).
                - Keyword analysis with insights on optimization strategies.
            """),
            expected_output="Markdown summary of metadata, keyword comparisons, and SEM insights.",
            agent=agent
        )

    def keyword_similarity_task(self, agent, our_keywords, competitor_keywords):
        return Task(
            description=dedent(f"""
                Compare keywords using TF-IDF and cosine similarity.
                Provide scores and insights into keyword overlaps and gaps.

                Keywords:
                - Our Keywords: {', '.join(our_keywords)}
                - Competitor Keywords: {', '.join(competitor_keywords)}

                Deliverables:
                1. TF-IDF scores and cosine similarity results.
                2. Categorization as Low, Medium, or High similarity.
                3. Recommendations for keyword optimization.

                Expected Output:
                - Similarity analysis with scores.
                - Recommendations for keyword enhancements.
            """),
            expected_output="Plain text summary of similarity scores and keyword recommendations.",
            agent=agent
        )

    def keyword_visualization_task(self, agent, tfidf_matrix, feature_names, top_n=5):
        return Task(
            description=dedent(f"""
                Generate visualizations for keyword distribution based on TF-IDF scores.
                Highlight the top {top_n} keywords for both websites.

                Deliverables:
                1. Visual plots comparing keyword distributions.
                2. Insights into optimization opportunities.

                Expected Output:
                - Plots and explanations of keyword differences.
            """),
            expected_output=f"Graphical visualizations of top {top_n} keywords with insights.",
            agent=agent
        )

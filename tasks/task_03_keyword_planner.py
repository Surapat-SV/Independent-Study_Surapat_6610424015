from crewai import Task
from textwrap import dedent
from datetime import date

class KeywordPlannerTasks:

    def keyword_discovery_task(self, agent, query_input):
        return Task(
            description=dedent(f"""
                Perform keyword discovery using BigQuery and internet search tools.
                Query databases for keywords related to the input topic and identify
                high-potential keywords based on relevance, search volume, and competition level.

                Analysis Steps:
                1. Use BigQuery to fetch keyword data for {query_input}.
                2. Analyze search volume, CPC, and competition metrics.
                3. Filter and rank keywords based on performance indicators.
                4. Treat 'N/A', '--', and '∞' values in metrics as '0' during analysis.

                User Input: {query_input}
            """),
            expected_output="A ranked list of keywords with metrics such as search volume, CPC, and competition level.",
            agent=agent
        )

    def keyword_categorization_task(self, agent, keywords):
        return Task(
            description=dedent(f"""
                Categorize discovered keywords into themes and match types (Broad, Phrase, Exact).
                Group keywords based on search intent, relevance, and performance metrics.

                Analysis Steps:
                1. Classify keywords by intent: informational, navigational, and transactional.
                2. Map each keyword to match types (Broad, Phrase, Exact) for targeting flexibility.
                3. Highlight primary and secondary keywords for structuring campaigns.

                Keywords: {', '.join(keywords)}
            """),
            expected_output="Categorized keyword list with themes, match types, and targeting suggestions.",
            agent=agent
        )

    def keyword_competitor_analysis_task(self, agent, query_input, competitor_url):
        return Task(
            description=dedent(f"""
                Perform competitor analysis to compare keyword strategies.
                Analyze keyword overlap, gaps, and performance differences with competitor campaigns.

                Analysis Steps:
                1. Scrape competitor website at {competitor_url} for metadata and keywords.
                2. Compare competitor keywords with query input '{query_input}'.
                3. Identify keyword gaps, overlaps, and optimization opportunities.

                Competitor URL: {competitor_url}
            """),
            expected_output="Competitor analysis report highlighting keyword gaps and optimization opportunities.",
            agent=agent
        )

    def keyword_trend_analysis_task(self, agent, keyword):
        return Task(
            description=dedent(f"""
                Analyze keyword trends using BigQuery to track changes over time.
                Evaluate search volume, growth trends, and seasonality patterns.

                Analysis Steps:
                1. Retrieve trend data for {keyword} from BigQuery.
                2. Analyze short-term and long-term changes in search volume.
                3. Provide insights into seasonal fluctuations and emerging trends.
                4. Handle 'N/A', '--', and '∞' as '0' in trend metrics during analysis.

                Keyword: {keyword}
            """),
            expected_output="Keyword trend analysis report highlighting growth trends and seasonality insights.",
            agent=agent
        )

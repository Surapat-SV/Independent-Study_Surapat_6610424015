###############################################
# Ad Copywriter Tasks
# File: tasks/task_04_adcopy_writer.py
# Purpose: Defines tasks for generating Google Ads copy and SEM planner reports
###############################################

# Import required libraries
from crewai import Task  # Core CrewAI framework for tasks
from textwrap import dedent  # For multi-line string formatting

# Class: Ad Copywriter Tasks
class AdCopyWriterTasks:

    def ad_copywriter_task(self, agent):
        """
        Task: Generate compelling ad copy for Google Ads.
        Purpose: Create headlines and descriptions tailored to SEM strategies with keyword integration.
        """
        return Task(
            description=dedent(f"""
                Generate Google Ads text copy, including headlines and descriptions.
                Ensure adherence to character limits and alignment with SEM strategies.
                Incorporate keywords extracted from business analysis, website analysis, and keyword planning.

                Analysis Steps:
                1. Use keywords and insights provided by:
                   - Business Analysis for audience targeting and goals.
                   - Website Analysis for metadata and SEO optimization.
                   - Keyword Planning for targeted keywords and match types.
                2. Generate 5 headlines, each within 30 characters.
                3. Generate 5 descriptions, each within 90 characters.
                4. Optimize text for clarity, relevance, and engagement.

                Output Requirements:
                - Headline and description pairs that align with ad strategies.
                - Ensure output uses markdown format with bullet points for readability.
            """),
            expected_output="5 Headlines (30 characters each) and 5 Descriptions (90 characters each) optimized for SEM strategies in markdown format.",
            agent=agent
        )

    def full_planner_task(self, agent):
        """
        Task: Compile a comprehensive SEM planner report.
        Purpose: Integrate outputs from all agents to create a cohesive SEM strategy.
        """
        return Task(
            description=dedent(f"""
                Compile a full SEM planner report integrating outputs from:
                - Business Analysis: Audience insights and goals.
                - Website Analysis: SEO data and keyword optimization.
                - Keyword Planning: Keyword categorization and trends.
                - Ad Copywriting: Headlines and descriptions.

                Deliverables:
                1. Organize findings into sections for each analysis component.
                2. Highlight key insights, trends, and recommendations.
                3. Format the final report in markdown for readability and presentation.
            """),
            expected_output="Complete SEM planner report formatted as markdown, integrating all agent outputs and recommendations.",
            agent=agent
        )

# End of file: tasks/task_04_adcopy_writer.py

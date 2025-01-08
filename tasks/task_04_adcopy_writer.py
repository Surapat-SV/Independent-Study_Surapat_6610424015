from crewai import Task
from textwrap import dedent
from datetime import date


class AdCopyWriterTasks:

    def ad_copywriter_task(self, agent):
        return Task(
            description=dedent(f"""
                Generate Google Ads text copy, including headlines and descriptions in Thai language.
                Ensure adherence to character limits and relevance to SEM strategy.

                Output Requirements:
                - Provide 5 headlines, each within 30 characters.
                - Provide 5 descriptions, each within 90 characters.
                - Ensure content aligns with target keywords and ad strategies.
            """),
            expected_output="5 Headlines (30 characters each) and 5 Descriptions (90 characters each) suitable for Google Ads in Thai language.",
            agent=agent
        )

    def full_planner_task(self, agent):
        return Task(
            description=dedent(f"""
                Compile a full SEM planner report.
                Integrate outputs from all agents including business analysis, website analysis, keyword planning, and ad copywriting.
                Present the final report in markdown format.
            """),
            expected_output="Complete SEM planner report formatted as markdown, integrating all agent outputs.",
            agent=agent
        )

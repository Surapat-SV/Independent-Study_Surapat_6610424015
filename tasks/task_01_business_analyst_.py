from crewai import Task
from textwrap import dedent
from datetime import date

class BusinessAnalystTasks:

    def business_analysis_task(self, agent, user_input):
        return Task(
            description=dedent(f"""
                Extract and analyze business details from the provided input.
                Focus on defining the business overview, target audience, and product/service details.
                Provide a concise summary in JSON format.

                User Input: {user_input}
            """),
            expected_output="JSON format with concise details about business overview, target audience, and product/service details.",
            agent=agent
        )

    def conversational_gathering_task(self, agent, context):
        """
        Task for dynamically asking questions to gather business insights.
        """
        return Task(
            description=dedent(f"""
                Engage in a structured conversation to gather detailed information about the user's business.
                Ask the following questions step-by-step:
                1. What is the name of your business?
                2. What products or services do you offer?
                3. Who is your target audience? Describe their demographics and preferences.
                4. What makes your product/service unique? Highlight your unique value proposition.
                5. What are your key marketing goals? Examples: Increase brand awareness, boost sales, etc.

                Ensure each question is followed by clarifying responses based on user inputs.

                Context: {context}
            """),
            expected_output="Structured details about business name, products/services, target audience, unique value proposition, and marketing goals.",
            agent=agent
        )

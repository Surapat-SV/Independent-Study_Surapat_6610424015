import streamlit as st
from agents.agent_01_business_analyst import create_business_analyst_agents
from tasks.task_01_business_analyst import create_business_analyst_tasks

def run_business_analyst():
    st.title("📋 Business Analyst")
    
    # User input
    business_name = st.text_input("Enter the business name:")
    product_service = st.text_area("Describe the product or service:")
    target_audience = st.text_area("Describe the target audience:")

    if st.button("Generate Business Analysis"):
        if business_name and product_service and target_audience:
            # Create agents
            senior_research_business_analyst, senior_writer_business_analyst = create_business_analyst_agents()

            # Create tasks
            research_task, writing_task = create_business_analyst_tasks(
                senior_research_business_analyst,
                senior_writer_business_analyst,
                business_name,
                product_service,
                target_audience
            )

            # Display research task and writing task descriptions
            st.subheader("Research Task Description")
            st.markdown(research_task.description)

            st.subheader("Writing Task Description")
            st.markdown(writing_task.description)
        else:
            st.warning("Please fill in all fields before generating the analysis.")

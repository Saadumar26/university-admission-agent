import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import streamlit as st

from programs import PROGRAMS

from agents.requirements_agent import run_requirements_agent
from agents.eligibility_agent import run_eligibility_agent
from agents.recommendation_agent import run_recommendation_agent


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="University Admission AI",
    page_icon="🎓",
    layout="wide",
)


# ---------------------------------------------------------
# Check API Key
# ---------------------------------------------------------

if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

else:
    st.error(
        "GROQ_API_KEY is missing. "
        "Please add it in Streamlit Secrets."
    )
    st.stop()


# ---------------------------------------------------------
# Title
# ---------------------------------------------------------

st.title("🎓 University Admission AI")

st.write(
    "A simple multi-agent university admission assistant "
    "built with CrewAI, Groq and Streamlit."
)

st.info(
    "This system follows common Pakistani academic qualifications "
    "such as Matric, Intermediate/HSSC, Bachelor's and Master's. "
    "The program requirements in this demo are sample data."
)


# ---------------------------------------------------------
# Student Information
# ---------------------------------------------------------

st.header("👤 Student Information")


col1, col2 = st.columns(2)


with col1:

    name = st.text_input(
        "Name",
        placeholder="Muhammad Saad Umar"
    )

    qualification = st.selectbox(
        "Current / Highest Qualification",
        [
            "Matric / SSC",
            "Intermediate / HSSC",
            "Bachelor's",
            "Master's",
        ]
    )

    field = st.text_input(
        "Field / Major",
        placeholder="Information Technology"
    )

    cgpa = st.number_input(
        "CGPA",
        min_value=0.0,
        max_value=4.0,
        value=0.0,
        step=0.01
    )


with col2:

    percentage = st.number_input(
        "Percentage (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.1
    )

    target_degree = st.selectbox(
        "Target Degree",
        [
            "BS",
            "MS",
            "PhD",
        ]
    )

    english = st.text_input(
        "English Proficiency",
        placeholder="PTE 56 / IELTS 6.5 / Not taken"
    )

    entry_test = st.text_input(
        "Entry Test",
        placeholder="NAT / GAT / University Test / Not taken"
    )


interests = st.text_area(
    "Academic Interests",
    placeholder="Artificial Intelligence, NLP, Machine Learning"
)

career_goal = st.text_area(
    "Career Goal",
    placeholder="AI Research Scientist"
)


# ---------------------------------------------------------
# Analyze Button
# ---------------------------------------------------------

if st.button(
    "🚀 Analyze My Admission",
    type="primary",
    use_container_width=True
):

    if not field.strip():
        st.warning("Please enter your field / major.")
        st.stop()

    applicant = {
        "name": name,
        "qualification": qualification,
        "field": field,
        "cgpa": cgpa,
        "percentage": percentage,
        "target_degree": target_degree,
        "english_proficiency": english,
        "entry_test": entry_test,
        "academic_interests": interests,
        "career_goal": career_goal,
    }

    applicant_text = json.dumps(
        applicant,
        indent=2
    )

    programs_text = json.dumps(
        PROGRAMS,
        indent=2
    )

    # -----------------------------------------------------
    # Run agents in parallel
    # -----------------------------------------------------

    st.divider()

    st.subheader("🤖 AI Agents")

    results = {}

    progress = st.empty()

    progress.info(
        "Running the three admission agents in parallel..."
    )

    agent_functions = {
        "requirements": run_requirements_agent,
        "eligibility": run_eligibility_agent,
        "recommendation": run_recommendation_agent,
    }

    with ThreadPoolExecutor(max_workers=3) as executor:

        futures = {
            executor.submit(
                function,
                applicant_text,
                programs_text
            ): name

            for name, function in agent_functions.items()
        }

        for future in as_completed(futures):

            agent_name = futures[future]

            try:
                results[agent_name] = future.result()

            except Exception as e:
                results[agent_name] = (
                    f"Agent failed: {str(e)}"
                )

    progress.success(
        "All three agents have completed their analysis."
    )

    # -----------------------------------------------------
    # Display Results
    # -----------------------------------------------------

    st.divider()

    st.header("📋 Admission Analysis")

    tab1, tab2, tab3 = st.tabs(
        [
            "📚 Requirements",
            "✅ Eligibility",
            "🎯 Recommendations",
        ]
    )

    with tab1:

        st.subheader(
            "Requirements Agent"
        )

        st.markdown(
            results.get(
                "requirements",
                "No result available."
            )
        )

    with tab2:

        st.subheader(
            "Eligibility Agent"
        )

        st.markdown(
            results.get(
                "eligibility",
                "No result available."
            )
        )

    with tab3:

        st.subheader(
            "Recommendation Agent"
        )

        st.markdown(
            results.get(
                "recommendation",
                "No result available."
            )
        )


# ---------------------------------------------------------
# Program Information
# ---------------------------------------------------------

with st.expander("📚 View Demo Program Data"):

    for program in PROGRAMS:

        st.write(
            f"**{program['university']} — "
            f"{program['program']}**"
        )

        st.json(program)


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.divider()

st.caption(
    "This application provides informational guidance only. "
    "Always verify admission requirements with the official "
    "university before applying."
)

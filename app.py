import os
from concurrent.futures import ThreadPoolExecutor

import streamlit as st

from requirements_agent import run_requirements_agent
from eligibility_agent import run_eligibility_agent
from recommendation_agent import run_recommendation_agent
from programs import PROGRAMS


# ---------------------------------------------------------
# Streamlit configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="University Admission Agent",
    page_icon="🎓",
    layout="wide"
)


# ---------------------------------------------------------
# Load Groq API Key
# ---------------------------------------------------------

if "GROQ_API_KEY" not in st.secrets:
    st.error(
        "GROQ_API_KEY is missing. "
        "Please add it in Streamlit Cloud → Manage app → Settings → Secrets."
    )
    st.stop()

os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]


# ---------------------------------------------------------
# App Title
# ---------------------------------------------------------

st.title("🎓 University Admission Agent")

st.write(
    """
    This application uses three independent AI agents to analyze
    university admission information.

    **Requirements Agent** → Explains admission requirements  
    **Eligibility Agent** → Evaluates student eligibility  
    **Recommendation Agent** → Recommends suitable programs
    """
)


# ---------------------------------------------------------
# Student Profile
# ---------------------------------------------------------

st.header("👨‍🎓 Student Profile")


col1, col2 = st.columns(2)


with col1:

    name = st.text_input(
        "Student Name",
        placeholder="e.g. Muhammad Saad Umar"
    )

    qualification = st.selectbox(
        "Highest Qualification",
        [
            "Matric / SSC",
            "Intermediate / HSSC",
            "Bachelor's",
            "Master's"
        ]
    )

    field = st.text_input(
        "Field / Major",
        placeholder="e.g. Computer Science, Information Technology"
    )

    cgpa = st.number_input(
        "CGPA",
        min_value=0.0,
        max_value=4.0,
        value=0.0,
        step=0.01
    )

    percentage = st.number_input(
        "Percentage",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.1
    )


with col2:

    target_degree = st.selectbox(
        "Target Degree",
        [
            "BS",
            "MS",
            "PhD"
        ]
    )

    english_proficiency = st.text_input(
        "English Proficiency",
        placeholder="e.g. IELTS 6.5, PTE 56, TOEFL 90"
    )

    entry_test = st.text_input(
        "Entry Test",
        placeholder="e.g. University Entry Test / Not Taken"
    )

    academic_interests = st.text_area(
        "Academic Interests",
        placeholder="e.g. Artificial Intelligence, NLP, Machine Learning"
    )

    career_goal = st.text_area(
        "Career Goal",
        placeholder="e.g. AI Research Scientist"
    )


# ---------------------------------------------------------
# Create Student Profile
# ---------------------------------------------------------

student_profile = {
    "name": name,
    "highest_qualification": qualification,
    "field_or_major": field,
    "cgpa": cgpa,
    "percentage": percentage,
    "target_degree": target_degree,
    "english_proficiency": english_proficiency,
    "entry_test": entry_test,
    "academic_interests": academic_interests,
    "career_goal": career_goal
}


# ---------------------------------------------------------
# Analyze Button
# ---------------------------------------------------------

if st.button(
    "🔍 Analyze Admission",
    type="primary",
    use_container_width=True
):

    # Basic validation

    if not name:
        st.warning("Please enter the student's name.")

    elif not field:
        st.warning("Please enter the student's field / major.")

    else:

        st.info(
            "The three agents are analyzing the student profile independently..."
        )

        # -------------------------------------------------
        # Run all three agents in parallel
        # -------------------------------------------------

        with ThreadPoolExecutor(max_workers=3) as executor:

            requirements_future = executor.submit(
                run_requirements_agent,
                student_profile,
                PROGRAMS
            )

            eligibility_future = executor.submit(
                run_eligibility_agent,
                student_profile,
                PROGRAMS
            )

            recommendation_future = executor.submit(
                run_recommendation_agent,
                student_profile,
                PROGRAMS
            )

            # Get results

            requirements_result = requirements_future.result()

            eligibility_result = eligibility_future.result()

            recommendation_result = recommendation_future.result()


        # -------------------------------------------------
        # Display Results
        # -------------------------------------------------

        st.success("Analysis completed successfully! 🎉")

        tab1, tab2, tab3 = st.tabs(
            [
                "📋 Requirements",
                "✅ Eligibility",
                "🎯 Recommendations"
            ]
        )


        with tab1:

            st.subheader("Admission Requirements")

            st.write(requirements_result)


        with tab2:

            st.subheader("Eligibility Assessment")

            st.write(eligibility_result)


        with tab3:

            st.subheader("Program Recommendations")

            st.write(recommendation_result)

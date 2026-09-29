import os
import streamlit as st

from requirements_agent import run_requirements_agent
from eligibility_agent import run_eligibility_agent
from recommendation_agent import run_recommendation_agent
from programs import PROGRAMS


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="University Admission Agent",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main page */
    .main {
        padding-top: 1rem;
    }

    /* Hide default Streamlit elements */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* Hero section */
    .hero {
        padding: 2rem 2rem 1.8rem 2rem;
        border-radius: 20px;
        background: linear-gradient(
            135deg,
            #0f172a 0%,
            #1e293b 50%,
            #334155 100%
        );
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
    }

    .hero h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }

    .hero p {
        font-size: 1.05rem;
        color: #cbd5e1;
        margin-bottom: 0;
    }

    /* Section titles */
    .section-title {
        font-size: 1.35rem;
        font-weight: 650;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
        color: #0f172a;
    }

    /* Information cards */
    .info-card {
        padding: 1rem 1.2rem;
        border-radius: 14px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        margin-bottom: 0.8rem;
    }

    .info-card-title {
        font-size: 0.82rem;
        color: #64748b;
        margin-bottom: 0.25rem;
    }

    .info-card-value {
        font-size: 1.15rem;
        font-weight: 650;
        color: #0f172a;
    }

    /* Agent cards */
    .agent-card {
        padding: 1.3rem;
        border-radius: 16px;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        min-height: 150px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
    }

    .agent-icon {
        font-size: 1.8rem;
        margin-bottom: 0.4rem;
    }

    .agent-title {
        font-size: 1.05rem;
        font-weight: 650;
        color: #0f172a;
    }

    .agent-description {
        color: #64748b;
        font-size: 0.9rem;
        line-height: 1.5;
    }

    /* Result box */
    .result-header {
        padding: 1rem 1.2rem;
        border-radius: 12px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        border-right: 1px solid #e2e8f0;
    }

    /* Button */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        padding: 0.7rem 1rem;
        font-weight: 650;
        font-size: 1rem;
    }

    /* Divider */
    .soft-divider {
        margin: 1.5rem 0;
        border-top: 1px solid #e2e8f0;
    }

    /* Small badge */
    .badge {
        display: inline-block;
        padding: 0.35rem 0.7rem;
        border-radius: 999px;
        background: #e2e8f0;
        color: #334155;
        font-size: 0.78rem;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# GROQ API KEY
# ============================================================

if "GROQ_API_KEY" not in st.secrets:
    st.error(
        "GROQ_API_KEY is missing. "
        "Please add it in Streamlit Cloud → Manage app → Settings → Secrets."
    )
    st.stop()

os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    """
    <div class="hero">
        <h1>🎓 University Admission Agent</h1>
        <p>
            A simple multi-agent system that analyzes admission requirements,
            evaluates eligibility, and recommends suitable programs.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR - STUDENT PROFILE
# ============================================================

with st.sidebar:

    st.markdown("## 👤 Student Profile")
    st.caption("Enter your academic information below.")

    st.markdown("---")

    name = st.text_input(
        "Full Name",
        placeholder="e.g. Muhammad Saad Umar",
    )

    highest_qualification = st.selectbox(
        "Highest Qualification",
        [
            "Matric / SSC",
            "Intermediate / HSSC",
            "Bachelor's",
            "Master's",
        ],
    )

    field = st.text_input(
        "Field / Major",
        placeholder="e.g. Information Technology",
    )

    col1, col2 = st.columns(2)

    with col1:
        cgpa = st.number_input(
            "CGPA",
            min_value=0.0,
            max_value=4.0,
            value=0.0,
            step=0.01,
            format="%.2f",
        )

    with col2:
        percentage = st.number_input(
            "Percentage",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.1,
            format="%.1f",
        )

    target_degree = st.selectbox(
        "Target Degree",
        [
            "BS",
            "MS",
            "PhD",
        ],
    )

    entry_test = st.text_input(
        "Entry Test",
        placeholder="e.g. NTS / University Test / Not Taken",
    )

    academic_interests = st.text_area(
        "Academic Interests",
        placeholder=(
            "e.g. Artificial Intelligence, "
            "Machine Learning, NLP"
        ),
        height=90,
    )

    career_goal = st.text_area(
        "Career Goal",
        placeholder=(
            "e.g. AI Research Scientist, "
            "Machine Learning Engineer"
        ),
        height=90,
    )

    st.markdown("---")

    analyze_button = st.button(
        "🚀 Analyze Admission",
        type="primary",
        use_container_width=True,
    )


# ============================================================
# MAIN INFORMATION
# ============================================================

st.markdown(
    '<div class="section-title">🤖 Your AI Admission Team</div>',
    unsafe_allow_html=True,
)

agent_col1, agent_col2, agent_col3 = st.columns(3)

with agent_col1:
    st.markdown(
        """
        <div class="agent-card">
            <div class="agent-icon">📋</div>
            <div class="agent-title">Requirements Agent</div>
            <div class="agent-description">
                Explains the admission requirements of available programs
                using the provided university data.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with agent_col2:
    st.markdown(
        """
        <div class="agent-card">
            <div class="agent-icon">✅</div>
            <div class="agent-title">Eligibility Agent</div>
            <div class="agent-description">
                Compares your academic profile with program requirements
                and determines your apparent eligibility.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with agent_col3:
    st.markdown(
        """
        <div class="agent-card">
            <div class="agent-icon">🎯</div>
            <div class="agent-title">Recommendation Agent</div>
            <div class="agent-description">
                Identifies programs that match your academic background,
                interests, and career goals.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    '<div class="soft-divider"></div>',
    unsafe_allow_html=True,
)


# ============================================================
# PROFILE PREVIEW
# ============================================================

st.markdown(
    '<div class="section-title">📊 Profile Overview</div>',
    unsafe_allow_html=True,
)

preview_col1, preview_col2, preview_col3, preview_col4 = st.columns(4)

with preview_col1:
    st.markdown(
        f"""
        <div class="info-card">
            <div class="info-card-title">Qualification</div>
            <div class="info-card-value">
                {highest_qualification}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with preview_col2:
    st.markdown(
        f"""
        <div class="info-card">
            <div class="info-card-title">Field / Major</div>
            <div class="info-card-value">
                {field if field else "Not provided"}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with preview_col3:
    st.markdown(
        f"""
        <div class="info-card">
            <div class="info-card-title">CGPA</div>
            <div class="info-card-value">
                {cgpa:.2f} / 4.00
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with preview_col4:
    st.markdown(
        f"""
        <div class="info-card">
            <div class="info-card-title">Target Degree</div>
            <div class="info-card-value">
                {target_degree}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# ANALYSIS
# ============================================================

if analyze_button:

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    if not name.strip():
        st.warning("Please enter your full name.")

    elif not field.strip():
        st.warning("Please enter your field / major.")

    else:

        # ----------------------------------------------------
        # Student Profile
        # ----------------------------------------------------

        student_profile = {
            "Name": name,
            "Highest Qualification": highest_qualification,
            "Field / Major": field,
            "CGPA": cgpa,
            "Percentage": percentage,
            "Target Degree": target_degree,
            "Entry Test": entry_test,
            "Academic Interests": academic_interests,
            "Career Goal": career_goal,
        }

        # ----------------------------------------------------
        # Agent 1 - Requirements
        # ----------------------------------------------------

        with st.spinner(
            "📋 Requirements Agent is analyzing programs..."
        ):
            requirements_result = run_requirements_agent(
                student_profile,
                PROGRAMS,
            )

        # ----------------------------------------------------
        # Agent 2 - Eligibility
        # ----------------------------------------------------

        with st.spinner(
            "✅ Eligibility Agent is evaluating your profile..."
        ):
            eligibility_result = run_eligibility_agent(
                student_profile,
                PROGRAMS,
            )

        # ----------------------------------------------------
        # Agent 3 - Recommendation
        # ----------------------------------------------------

        with st.spinner(
            "🎯 Recommendation Agent is finding suitable programs..."
        ):
            recommendation_result = run_recommendation_agent(
                student_profile,
                PROGRAMS,
            )

        # ----------------------------------------------------
        # Results
        # ----------------------------------------------------

        st.success("Analysis completed successfully! 🎉")

        st.markdown(
            '<div class="section-title">📑 Admission Analysis</div>',
            unsafe_allow_html=True,
        )

        tab1, tab2, tab3 = st.tabs(
            [
                "📋 Requirements",
                "✅ Eligibility",
                "🎯 Recommendations",
            ]
        )

        # ----------------------------------------------------
        # Requirements Tab
        # ----------------------------------------------------

        with tab1:

            st.markdown(
                """
                <div class="result-header">
                    <strong>Admission Requirements</strong><br>
                    <span style="color:#64748b;">
                    Requirements identified from the provided program data.
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.write(requirements_result)

        # ----------------------------------------------------
        # Eligibility Tab
        # ----------------------------------------------------

        with tab2:

            st.markdown(
                """
                <div class="result-header">
                    <strong>Eligibility Assessment</strong><br>
                    <span style="color:#64748b;">
                    This assessment indicates apparent eligibility based
                    only on the provided information.
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.write(eligibility_result)

        # ----------------------------------------------------
        # Recommendation Tab
        # ----------------------------------------------------

        with tab3:

            st.markdown(
                """
                <div class="result-header">
                    <strong>Program Recommendations</strong><br>
                    <span style="color:#64748b;">
                    Programs matched to your academic background,
                    interests, and career goals.
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.write(recommendation_result)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#94a3b8;
        padding:2rem 0 1rem 0;
        font-size:0.85rem;
    ">
        Built with Streamlit + CrewAI + Groq
        <br>
        Multi-Agent University Admission System
    </div>
    """,
    unsafe_allow_html=True,
)

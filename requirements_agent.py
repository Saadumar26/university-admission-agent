import os

from crewai import Agent, Task, Crew, LLM


def run_requirements_agent(applicant_profile, programs):
    """
    Run the Admission Requirements Agent.
    """

    llm = LLM(
        model="groq/openai/gpt-oss-120b",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.2,
    )

    requirements_agent = Agent(
        role="University Admission Requirements Analyst",

        goal=(
            "Analyze the provided university programs and identify "
            "the admission requirements relevant to the student."
        ),

        backstory=(
            "You are an admission requirements specialist familiar "
            "with the Pakistani education system. You understand "
            "Matric, Intermediate/HSSC, Bachelor's and Master's "
            "qualifications. You carefully examine the provided "
            "program information and never invent requirements."
        ),

        llm=llm,

        allow_delegation=False,

        verbose=False,
    )

    task = Task(
        description=f"""
        Analyze the university programs provided below.

        STUDENT PROFILE:
        {applicant_profile}

        AVAILABLE PROGRAMS:
        {programs}

        Identify the admission requirements relevant to this student.

        For each relevant program, explain:

        1. Required academic qualification
        2. Minimum CGPA or percentage
        3. Required academic background
        4. Entry test requirement
        5. English language requirement

        Important rules:

        - Use ONLY the information provided.
        - Do not invent university requirements.
        - If information is missing, clearly say:
          "Not specified in the provided data."
        - Consider the Pakistani education system.
        - GRE and GMAT should NOT be added unless explicitly
          present in the provided program data.
        - Keep the explanation simple and beginner-friendly.
        """,

        expected_output="""
        A clear program-by-program summary of admission requirements.
        Mention missing information explicitly.
        """,

        agent=requirements_agent,
    )

    crew = Crew(
        agents=[requirements_agent],
        tasks=[task],
        verbose=False,
    )

    result = crew.kickoff()

    return str(result)

import os

from crewai import Agent, Task, Crew, LLM


def run_recommendation_agent(applicant_profile, programs):
    """
    Run the Program Recommendation Agent.
    """

    llm = LLM(
        model="groq/openai/gpt-oss-120b",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.4,
    )

    recommendation_agent = Agent(
        role="Academic Program Recommendation Specialist",

        goal=(
            "Identify university programs that match the student's "
            "academic background, target degree, interests and career goals."
        ),

        backstory=(
            "You are an academic program advisor. You understand "
            "Pakistani academic qualifications and computing-related "
            "university programs. You recommend programs based only "
            "on the student's information and the programs provided."
        ),

        llm=llm,

        allow_delegation=False,

        verbose=False,
    )

    task = Task(
        description=f"""
        Recommend suitable university programs for this student.

        STUDENT PROFILE:
        {applicant_profile}

        AVAILABLE PROGRAMS:
        {programs}

        Consider:

        1. Current qualification
        2. Field / major
        3. CGPA
        4. Percentage
        5. Target degree
        6. Academic interests
        7. Career goals

        For each suitable program, explain:

        - Why it matches the student's academic background
        - Why it matches the student's interests
        - Any important requirement the student should verify

        Important rules:

        - Do not guarantee admission.
        - Do not invent university requirements.
        - Do not claim a program is officially approved for the student.
        - Do not use GRE or GMAT unless explicitly included in
          the provided program information.
        - If the student's information is insufficient, say so.
        - Keep the recommendation practical and easy to understand.
        """,

        expected_output="""
        A simple list of suitable programs with short explanations
        showing why each program matches the student's profile.
        """,

        agent=recommendation_agent,
    )

    crew = Crew(
        agents=[recommendation_agent],
        tasks=[task],
        verbose=False,
    )

    result = crew.kickoff()

    return str(result)

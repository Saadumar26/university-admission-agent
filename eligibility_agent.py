import os

from crewai import Agent, Task, Crew, LLM


def run_eligibility_agent(applicant_profile, programs):
    """
    Run the Eligibility Agent.
    """

    llm = LLM(
        model="groq/openai/gpt-oss-120b",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.2,
    )

    eligibility_agent = Agent(
        role="University Eligibility Evaluator",

        goal=(
            "Evaluate the student's eligibility for the provided "
            "university programs."
        ),

        backstory=(
            "You are an academic eligibility evaluator familiar "
            "with the Pakistani education system. You compare "
            "student qualifications with the admission requirements "
            "provided for each program. You do not make assumptions "
            "when information is missing."
        ),

        llm=llm,

        allow_delegation=False,

        verbose=False,
    )

    task = Task(
        description=f"""
        Evaluate the student's eligibility for the available
        university programs.

        STUDENT PROFILE:
        {applicant_profile}

        AVAILABLE PROGRAMS:
        {programs}

        For each relevant program, classify the student's status as:

        - Appears Eligible
        - Appears Not Eligible
        - Cannot Determine

        Consider:

        1. Current qualification
        2. Field / major
        3. CGPA
        4. Percentage
        5. Target degree
        6. Entry test
        7. English proficiency

        Important rules:

        - Use ONLY the provided program requirements.
        - Do not invent requirements.
        - Do not assume that missing information satisfies a requirement.
        - If an important requirement is unknown, use
          "Cannot Determine".
        - Do not use GRE or GMAT unless they are explicitly listed
          in the provided program requirements.
        - Explain the reason for each result.
        - Keep the answer simple.
        """,

        expected_output="""
        A program-by-program eligibility assessment containing:
        program name, eligibility status, and a short explanation.
        """,

        agent=eligibility_agent,
    )

    crew = Crew(
        agents=[eligibility_agent],
        tasks=[task],
        verbose=False,
    )

    result = crew.kickoff()

    return str(result)

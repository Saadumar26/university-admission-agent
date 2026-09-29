import os

from crewai import Agent, Task, Crew, LLM


def run_eligibility_agent(applicant_profile, programs):
    """
    Eligibility Agent:
    Evaluates whether the student appears eligible.
    """

    llm = LLM(
        model="groq/openai/gpt-oss-120b",
        api_key=os.environ["GROQ_API_KEY"],
        temperature=0.2,
        max_tokens=1200,
        reasoning_effort="low",
    )

    agent = Agent(
        role="University Eligibility Evaluator",

        goal=(
            "Evaluate the student's apparent eligibility for "
            "the provided university programs."
        ),

        backstory=(
            "You are an academic eligibility evaluator familiar "
            "with the Pakistani education system. You compare "
            "student qualifications against the requirements "
            "provided for each program."
        ),

        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    task = Task(
        description=f"""
        Evaluate the student's eligibility.

        STUDENT PROFILE:
        {applicant_profile}

        AVAILABLE PROGRAMS:
        {programs}

        For each relevant program, classify the student as:

        - Appears Eligible
        - Appears Not Eligible
        - Cannot Determine

        Consider:

        1. Qualification
        2. Field / major
        3. CGPA
        4. Percentage
        5. Target degree
        6. Entry test
        7. English proficiency

        Rules:

        - Use ONLY the provided requirements.
        - Never invent requirements.
        - Missing information must not automatically be treated
          as satisfying a requirement.
        - If important information is missing, use
          "Cannot Determine".
        - Do not introduce GRE or GMAT unless explicitly listed.
        - Give a short reason for each result.
        """,

        expected_output=(
            "A concise program-by-program eligibility assessment "
            "with status and explanation."
        ),

        agent=agent,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=False,
    )

    result = crew.kickoff()

    return str(result)

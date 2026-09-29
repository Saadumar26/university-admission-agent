import os

from crewai import Agent, Task, Crew, LLM


def run_recommendation_agent(applicant_profile, programs):
    """
    Recommendation Agent:
    Finds programs that match the student's background and interests.
    """

    llm = LLM(
        model="groq/openai/gpt-oss-120b",
        api_key=os.environ["GROQ_API_KEY"],
        temperature=0.3,
        max_tokens=1200,
        reasoning_effort="low",
    )

    agent = Agent(
        role="Academic Program Recommendation Specialist",

        goal=(
            "Identify university programs that match the student's "
            "academic background, interests and career goals."
        ),

        backstory=(
            "You are an academic program advisor familiar with "
            "Pakistani academic qualifications and university "
            "programs."
        ),

        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    task = Task(
        description=f"""
        Recommend suitable programs for this student.

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

        For every recommended program, explain briefly:

        - Why it matches the student's background
        - Why it matches the student's interests
        - Any requirement the student should verify

        Rules:

        - Do not guarantee admission.
        - Do not invent university requirements.
        - Do not introduce GRE or GMAT unless explicitly included
          in the provided program data.
        - If there is insufficient information, say so.
        - Keep the response concise.
        """,

        expected_output=(
            "A concise list of suitable programs with reasons "
            "for each recommendation."
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

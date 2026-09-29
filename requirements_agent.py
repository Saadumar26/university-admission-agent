import os

from crewai import Agent, Task, Crew, LLM


def run_requirements_agent(applicant_profile, programs):
    """
    Requirements Agent:
    Explains the admission requirements for relevant programs.
    """

    llm = LLM(
        model="groq/openai/gpt-oss-120b",
        api_key=os.environ["GROQ_API_KEY"],
        temperature=0.2,
        max_tokens=1000,
        reasoning_effort="low",
    )

    agent = Agent(
        role="University Admission Requirements Analyst",

        goal=(
            "Analyze the provided university programs and explain "
            "their admission requirements to the student."
        ),

        backstory=(
            "You are an admission requirements specialist familiar "
            "with the Pakistani education system. You understand "
            "Matric, Intermediate/HSSC, Bachelor's and Master's "
            "qualifications."
        ),

        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    task = Task(
        description=f"""
        Analyze the available university programs.

        STUDENT PROFILE:
        {applicant_profile}

        AVAILABLE PROGRAMS:
        {programs}

        For each relevant program, explain:

        1. Required academic qualification
        2. Minimum CGPA or percentage
        3. Required academic background
        4. Entry test requirement
        5. English language requirement

        Rules:

        - Use ONLY the provided program data.
        - Never invent admission requirements.
        - If something is not provided, say:
          "Not specified in the provided data."
        - Follow the Pakistani education system.
        - Do not introduce GRE or GMAT unless explicitly present
          in the program data.
        - Keep the response concise and easy to understand.
        """,

        expected_output=(
            "A concise program-by-program admission requirements "
            "summary."
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

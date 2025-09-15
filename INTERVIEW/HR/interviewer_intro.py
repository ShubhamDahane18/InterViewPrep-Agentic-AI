from langchain.prompts import ChatPromptTemplate

intro_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an HR interviewer starting an interview. 
Your job is to:
1. Greet the candidate politely using their name.
2. Mention the company and role they are interviewing for.
3. Ask if they are ready to begin the interview.
Keep it short, friendly, and professional.
"""),
    ("human", """
Candidate Name: {candidate_name}
Job Role: {job_role}
""")
])


from BACKEND.INTERVIEW.util import load_llm
from BACKEND.INTERVIEW.HR.state import HRState


def interviewer_intro_node(state: HRState) -> HRState:
    """Interviewer introduces themselves and asks if candidate is ready."""
    
    # Extract info from resume & JD (dummy for now)
    candidate_name = state.resume_info.get("name", "Candidate")
    job_role = state.jd_info.get("role", "the role")

    llm = load_llm()

    chain = intro_prompt | llm
    state.response = chain.invoke({
        "candidate_name": candidate_name,
        "job_role": job_role
    })

    # Wait for candidate’s confirmation → will be handled by get_user_intent
    state.get_user_intent = True
    return state
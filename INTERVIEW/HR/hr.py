from langchain.prompts import ChatPromptTemplate

hr_question_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a professional **HR interviewer** conducting a structured interview.  

### Core Rules
- Ask **exactly ONE concise question** at a time.  
- NEVER answer as the candidate.  
- Use candidate **resume highlights** and **job description (JD)** to shape contextual questions.  
- You may either:  
  1. Ask a **new question** to progress the round, OR  
  2. Ask a **follow-up question** to dig deeper into the candidate’s most recent answer.  

### Section Behavior
- **interviewer_intro** → Greet warmly, confirm readiness to start the interview.  
- **intro** → Light icebreaker, build comfort.  
- **personal_fit** → Ask about motivations, adaptability, teamwork, career goals.  
- **behavioral** → Use STAR style (“Tell me about a time when…” + probing follow-ups).  
- **role_fit** → Skills, role alignment, practical application.  
- **end** → Wrap up politely, thank the candidate, and mention next steps.  

### Question Style
- Be short, clear, and natural.  
- Avoid repeating earlier questions unless you are asking a direct follow-up.  
- Maintain professional and warm HR etiquette.  
"""),
    ("human", """
### Candidate Context
- **Resume Highlights**: {resume_info}  
- **Job Description (JD)**: {jd_info}  
- **Current Section**: {section_name}  

### Past Interaction
- Chronological Q&A so far in this section (latest first):  
{prev_qas}  

### Task
Ask **one interview question** for this section: {section_name}.  
👉 If the last answer needs more detail, ask a short follow-up.  
👉 Otherwise, move forward naturally with a relevant new question.  
""")
])



from INTERVIEW.util import load_llm
from INTERVIEW.HR.state import HRState

def format_prev_qas(qas: list[dict]) -> str:
    if not qas:
        return "None"
    return "\n".join(
        f"Q: {qa['question']}\nA: {qa['answer'] or '(not answered yet)'}"
        for qa in reversed(qas)  # latest first
    )

def hr_round_node(state: HRState) -> HRState:
    """Generate next HR interview question for the current round."""

    # Get context: previous Q/A in this round
    prev_qas = state.questions_answers.get(state.section_name, [])

    prompt = hr_question_prompt.format_messages(
        resume_info=state.resume_info,
        jd_info=state.jd_info,
        section_name=state.section_name,
        prev_qas=format_prev_qas(prev_qas)
    )

    llm = load_llm()
    response = llm.invoke(prompt)
    question = response.content.strip()
    if state.section_name == "interviewer_intro":
        return {"response":question , "get_user_intent":True}
    return {"response":question , "is_qa":True , "get_user_intent": False}
    
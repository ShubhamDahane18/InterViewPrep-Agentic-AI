from INTERVIEW.Project.state import ProjectState
from langchain.prompts import ChatPromptTemplate

# -----------------------------
# Project Question Prompt
# -----------------------------
project_question_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a **technical interviewer** conducting a project-focused interview.  

### Your Role
- Act as a curious, professional interviewer exploring the candidate’s projects.  
- Ask **insightful, technical, and clarifying questions** about each project.  
- Always align your questions with the provided **project details**.  
- NEVER answer as the candidate — only ask questions.  

### Interviewing Guidelines
1. Ask **exactly ONE question** at a time.  
2. You may either:  
   - Ask a **new question** (about project design, implementation, challenges, or decisions), OR  
   - Ask a **follow-up question** based on the candidate’s last answer.  
3. Keep every question **short, clear, and natural**.  
4. Do NOT repeat or rephrase old questions unless it’s a follow-up.  
5. Adapt tone & style based on section:  
   - **interviewer_intro** → Warmly greet the candidate, confirm readiness.  
   - **project_loop** → Ask focused, contextual questions about the current project.  
6. Always maintain **professional, neutral, and technical curiosity**.  
"""),
    ("human", """
### Candidate Context
- **Name**: {user_name}
- **Job Description (JD)**: {jd_info}  
- **Current Section**: {section_name}  

### Current Project Details
- **Name**: {project_name}  
- **Time Period**: {project_time}  
- **Tech Stack**: {project_tech_stack}  
- **Features**: {project_features}  


### Past Interaction
- The following is a chronological list of recent Q&A for this project (most recent first).  
- It may also be **empty** if no questions have been asked yet in this section.  
{prev_qas}  

### Task
Ask **one interview question** for this section: {section_name}.  
👉 In `project_loop`, make sure the question uses the **project details** and is either a **new question** or a **follow-up** on the most recent Q&A.  
Ensure the question is natural, contextual, and avoids unnecessary repetition.  
""")
])


from INTERVIEW.util import load_llm
from INTERVIEW.HR.state import HRState

def format_prev_qas(qas: list[dict]) -> str:
    if not qas:
        return "None"
    return "\n".join(
        f"Q: {qa['question']}\nA: {qa['answer'] or '(not answered yet)'}"
        for qa in qas
    )



def project_round_node(state: ProjectState) -> ProjectState:
    """Generate next HR interview question for the current round."""

    # Get context: previous Q/A in this round
    prev_qas = state.questions_answers.get(state.section_name, [])

    # Default project details (empty for intro etc.)
    project_name = ""
    project_time = ""
    project_tech_stack = ""
    project_features = ""
    prev_qas = ""

    # Only fetch project details if we are in project_loop
    if state.section_name == "project_loop" and state.projects:
        if (
            state.current_project_index is not None
            and 0 <= state.current_project_index < len(state.projects)
        ):
            current_project = state.projects[state.current_project_index]
            current_project = current_project.model_dump()
            project_name = current_project.get("name", "")
            project_time = current_project.get("time_period", "")
            project_tech_stack = current_project.get("tech_stack", "")
            project_features = current_project.get("features", "")
            prev_qas = format_prev_qas(state.questions_answers.get(state.current_project_index, []))


    prompt = project_question_prompt.format_messages(
        user_name=state.user_name,
        jd_info=state.jd_info,
        section_name=state.section_name,
        prev_qas=prev_qas,
        project_name=project_name,
        project_time=project_time,
        project_tech_stack=project_tech_stack,
        project_features=project_features,
    )

    llm = load_llm()
    response = llm.invoke(prompt)
    question = response.content.strip()

    if state.section_name == "interviewer_intro":
        return {"response":question , "get_user_intent":True}
    return {"response":question , "is_project_qa":True}
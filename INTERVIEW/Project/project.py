from INTERVIEW.Project.state import ProjectState
from langchain.prompts import ChatPromptTemplate

# -----------------------------
# Project Question Prompt (with Past Interaction Handling)
# -----------------------------
project_question_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a **technical interviewer** conducting a project-focused interview.  

### Your Role
- Act as a curious, professional interviewer exploring the candidate’s projects.  
- Ask **insightful, technical, and clarifying questions** about each project.  
- Always align your questions with the provided **project details**, **job description (JD)**, and the **candidate’s resume if available**.  
- NEVER answer as the candidate — only ask questions.  

### Interviewing Guidelines
1. Ask **exactly ONE question** at a time.  
2. You may either:  
   - Ask a **new question** (about project design, implementation, challenges, or decisions), OR  
   - Ask a **follow-up question** based on the candidate’s last answer (to dig deeper).  
3. Keep every question **short, clear, and natural**.  
4. Do NOT repeat or rephrase old questions unless it’s a follow-up.  
5. Adapt tone & style based on the section:  
   - **interviewer_intro** → Warm greeting, confirm readiness for the project discussion.  
   - **project_loop** → Ask focused, contextual, technical questions about the current project.  
   - **end** → Wrap up politely, thank them for discussing their projects, and guide to the next interview stage.  
6. Always maintain **professional HR etiquette**: neutral, unbiased, encouraging, but technically curious.  
7. **Strict flow rule**: The valid sequence is `["interviewer_intro", "project_loop", "end"]`.  
   - After `interviewer_intro`, move into `project_loop`.  
   - Stay in `project_loop` until candidate/project discussion is complete.  
   - Only then move to `end`. Never skip ahead or jump backwards.  
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
The following is a chronological list of recent Q&A for this project (most recent first).  
It may also be **empty** if no questions have been asked yet in this section.  
{prev_qas}  

### Task
Ask **one interview question** for the current section: {section_name}.  
👉 In `project_loop`, make sure the question leverages the **project details** and is either a **new technical question** OR a **follow-up** based on the candidate’s most recent answer.  
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
        for qa in reversed(qas)  # latest first
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
            int(state.current_project_index) is not None
            and 0 <= int(state.current_project_index) < len(state.projects)
        ):
            current_project = state.projects[int(state.current_project_index)]
            current_project = current_project.model_dump()
            project_name = current_project.get("name", "")
            project_time = current_project.get("time_period", "")
            project_tech_stack = current_project.get("tech_stack", "")
            project_features = current_project.get("features", "")
            prev_qas = format_prev_qas(state.questions_answers.get(int(state.current_project_index), []))


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
    return {"response":question , "is_project_qa":True , "get_user_intent": False}
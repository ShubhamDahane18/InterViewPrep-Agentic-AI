# -----------------------------
# Core Function
# -----------------------------
from INTERVIEW.HR.state import HRState
from INTERVIEW.TECHNICAL.state import TechRoundState
from INTERVIEW.HR.hr_graph import hr_graph
from app.db import save_hr_state, get_hr_state, get_hr_resume, get_jd,get_tech_resume ,get_candi_name, get_project_state , save_project_state , get_tech_state , save_tech_state , get_resume
from typing import Dict


def process_hr_query(email: str, user_input: str) -> str:
    """
    Process a user input for the HR agent:
    - If user doesn't exist, create empty state
    - Attach resume_info and jd_info if missing
    - Update state with Q&A
    - Return agent response + state
    """

    # Step 1: Fetch state
    state = get_hr_state(email)

    # Step 2: If no state exists, create new one
    if not state:
        state = HRState()
        save_hr_state(email, state)

    # Step 3: Attach resume_info if missing
    if not state.resume_info:
        resume_info = get_hr_resume(email)
        if resume_info:
            state.resume_info = resume_info

    # Step 4: Attach jd_info if missing (if job_id provided)
    if not state.jd_info:
        jd_info = get_jd(email)
        if jd_info:
            state.jd_info = jd_info

    # Step 5: Pass user input into state for HR graph
    state_dict = state.dict()
    state_dict["user_input"] = user_input

    # Run through HR graph/agent
    hr = hr_graph()
    state_out = hr.invoke(state_dict)

    # Convert back into HRState (preserves resume_info + jd_info)
    state = HRState(**state_out)

    # Step 6: Save updated state
    save_hr_state(email, state)

    # Step 7: Return
    return state.model_dump().get("response")



from INTERVIEW.Project.project_graph import Project_graph
from INTERVIEW.Project.state import ProjectState

def process_project_query(email: str, user_input: str) -> Dict:
    """
    Process user input for candidate projects.
    - Retrieve ProjectState
    - Attach projects from resume
    - Call project.invoke with state
    - Save updated state
    - Return response
    """
    state = get_project_state(email)

    if not state:
        # Initialize fresh state
        state = ProjectState()
        save_project_state(email, state.model_dump())

    # If still None, hard fail
    if not state:
        raise ValueError(f"No ProjectState found for {email}")

    # Load resume from DB
    resume = get_resume(email)

    if not state.jd_info:
        jd_info = get_jd(email)
        if jd_info:
            state.jd_info = jd_info

    # Update state dict with latest input + projects from resume
    state_dict = state.dict()
    state_dict["user_input"] = user_input

    if resume and "projects" in resume:
        state_dict["projects"] = resume["projects"]   # ✅ inject projects from resume

    if resume and "name" in resume:
        state_dict["user_name"] = resume["name"]   # ✅ inject name from resume


    # Call project graph
    project = Project_graph()
    state = project.invoke(state_dict)

    # Convert back into Pydantic model
    # state = ProjectState(**new_state)

    # Save updated state
    save_project_state(email, state)

    return state.get("response")
    

from INTERVIEW.TECHNICAL.tech_graph import tech_graph

def process_tech_query(email: str, user_input: str) -> str:
    """
    Process a user input for the HR agent:
    - If user doesn't exist, create empty state
    - Attach resume_info and jd_info if missing
    - Update state with Q&A
    - Return agent response + state
    """

    # Step 1: Fetch state
    state = get_tech_state(email)
    print("Getting State")
    # Step 2: If no state exists, create new one
    if not state:
        state = TechRoundState()
        save_tech_state(email, state)

    # Step 3: Attach resume_info if missing
    if not state.skills:
        resume_info = get_tech_resume(email)
        if resume_info:
            state.candidate_name = resume_info["name"]
            state.skills = resume_info["skills"]
        print("Skills added")

    # Step 4: Attach jd_info if missing (if job_id provided)
    if not state.job_info:
        jd_info = get_jd(email)
        if jd_info:
            state.job_info = jd_info 
        print('JD Acquired')
    

    # Step 5: Pass user input into state for Tech graph
    state_dict = state.model_dump() # Fixed: Use model_dump for Pydantic
    state_dict["user_input"] = user_input
    print('Passed User Input')

    # Run through Tech graph/agent
    tech = tech_graph()
    state_out = tech.invoke(state_dict)

    # Convert back into TechState (preserves resume_info + jd_info)
    state = TechRoundState(**state_out)

    # Step 6: Save updated state
    save_tech_state(email, state)

    # Step 7: Return
    return state.model_dump().get("response")

from INTERVIEW.EVALUATION.state import EvaluationState
from INTERVIEW.EVALUATION.evaluation_graph import build_evaluation_graph

def process_eval(round_name:str,email:str)->str:
    
    state = EvaluationState()    
    state['jd_info'] = get_jd(email)
    state['round_name'] = round_name
    state['candidate_name'] = get_candi_name(email)
    
    if round_name == 'HR':
        hr_state = get_hr_state(email)
        state['questions_answers'] = hr_state.questions_answers
    elif round_name=='Tech':
        tech_state = get_tech_state(email)
        state['questions_answers'] = tech_state.questions_answers
    else:
        pr_state = get_project_state(email)
        qa = pr_state.questions_answers
        project_name = []
        for project in pr_state.projects:
            project_name.append(project.name)
        
        old_keys = list(qa.keys())
        new_qa = {}
    
        for i, old_key in enumerate(old_keys):
            if i < len(project_name):
                new_key = project_name[i]
            else:
                new_key = old_key  # fallback if fewer project names than QA sections
            new_qa[new_key] = qa[old_key]
            state['questions_answers'] = new_qa
    
    eval = build_evaluation_graph()
    state_out = eval.invoke(state)
    
    return state_out['final_report']

        
        
        
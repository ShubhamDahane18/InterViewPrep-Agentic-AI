# -----------------------------
# Core Function
# -----------------------------
from INTERVIEW.HR.state import HRState
from INTERVIEW.HR.hr_graph import hr_graph
from INTERVIEW.Project import project_graph
from app.db import save_hr_state, get_hr_state, get_hr_resume, get_jd
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
    
    state.limit = 5

    # Step 5: Pass user input into state for HR graph
    state_dict = state.dict()
    state_dict["user_input"] = user_input

    # Run through HR graph/agent
    hr = hr_graph()
    state_out = hr.invoke(state_dict)

    # Convert back into HRState (preserves resume_info + jd_info)
    new_state = HRState(**state_out)

    # Step 6: Save updated state
    save_hr_state(email, new_state)

    # Step 7: Return
    return new_state.dict().get("response")


from INTERVIEW.Project.project_graph import Project_graph # assuming you have a project graph

def process_project_query(email: str, user_input: str) -> Dict:
    """
    Process user input for candidate projects.
    - Retrieve HRState
    - Iterate over projects
    - Call project.invoke with state + index
    - Save updated state
    - Return response
    """
    state = get_hr_state(email)
    if not state:
        raise ValueError(f"No HRState found for {email}")

    # Add user input into state
    state_dict = state.dict()
    state_dict["user_input"] = user_input

    # Iterate over projects
    responses = []
    projects = state.resume_info.get("projects", []) if state.resume_info else []
    
    project = Project_graph()
    new_state = project.invoke(state_dict)

    # Update state with project-specific changes
    state = HRState(**new_state)

    # Save final state
    save_hr_state(email, state)

    return {
        "responses": responses
    }
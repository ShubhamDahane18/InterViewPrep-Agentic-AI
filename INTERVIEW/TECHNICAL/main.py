from graph import build_graph
from state import TechRoundState, ExtractJobInfo
from io_utils import present_to_user
from db_helpers import get_jd

def fetch_job_info(candidate_email: str) -> ExtractJobInfo | None:
    jd_data = get_jd(candidate_email)
    if jd_data:
        return ExtractJobInfo(
            job_title=jd_data.get("job_title", "Unknown"),
            company=jd_data.get("company"),
            location=jd_data.get("location"),
            job_type=jd_data.get("job_type"),
            description=jd_data.get("description"),
            required_skills=jd_data.get("required_skills", [])
        )
    return None

def run_interview(candidate_email: str):
    initial_state: TechRoundState = {
        "company_name": "Google",
        "core_subjects": ["Data Structures and Algorithms", "Operating Systems", "Computer Networks"],
        "skills": {"programming_languages": ["Python", "Go"], "cloud_technologies": ["GCP"]},
        "core_qa": [],
        "tech_qa": [],
        "decision": {},
        "qa_counts": {},
        "questions_per_topic": 2,
        "max_questions_per_topic": 5,
        "followups_used": {"core": 0, "technical": 0},
        "job_info": None
    }

    # Fetch JD
    jd_info = fetch_job_info(candidate_email)
    if jd_info:
        initial_state["job_info"] = jd_info
        present_to_user(f"📄 Job Description loaded for {jd_info.job_title}")
    else:
        present_to_user("⚠️ No Job Description found. Questions will use available skills.")

    app = build_graph()
    print("--- Starting Technical Interview Simulation ---")
    for _ in app.stream(initial_state, {"recursion_limit": 100}):
        pass
    print("--- Interview Finished ---")

if __name__ == "__main__":
    run_interview("john@example.com")

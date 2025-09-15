# main.py
from graph import build_graph
from state import TechRoundState

def run_interview():
    initial_state: TechRoundState = {
    "company_name": "Google",
    "core_subjects": ["Data Structures and Algorithms", "Operating Systems", "Computer Networks"],
    "skills": {
        "programming_languages": ["Python", "Go"],
        "cloud_technologies": ["Google Cloud Platform (GCP)"]
    },
    "core_qa": [],
    "tech_qa": [],
    "evaluation": {},
    "decision": {},
    "summary": None,
    "qa_counts": {},
    "questions_per_topic": 2,      # baseline
    "max_questions_per_topic": 5   # absolute cap
}

    app = build_graph()
    print("--- Starting Technical Interview Simulation ---")
    for _ in app.stream(initial_state, {"recursion_limit": 100}):
        pass
    print("--- Interview Finished ---")

if __name__ == "__main__":
    run_interview()

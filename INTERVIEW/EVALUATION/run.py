from evaluation_graph import build_evaluation_graph
from state import EvaluationState

def run_interview():
    # Build the evaluation workflow graph
    workflow = build_evaluation_graph()

    # Initial candidate state
    state: EvaluationState = {
        "candidate_name": "John Doe",
        "candidate_email": "john@example.com",
        "company_name": "TechCorp",
        "rounds": [
            {
                "round_name": "Tech",
                "qa": [
                    {"question": "What is OOP?", "answer": "Object-oriented programming is based on classes and objects."}
                ]
            },
            {
                "round_name": "Project",
                "qa": [
                    {"question": "Describe your last project", "answer": "Built a neural network for image classification using TensorFlow."}
                ]
            }
        ]
    }

    print("--- Starting Interview Simulation ---\n")

    # Run the workflow and stream outputs
    final_state = state
    for chunk in workflow.stream(state, {"recursion_limit": 100}):
        # Only update final state if chunk is dict
        if isinstance(chunk, dict):
            final_state = chunk

    print("\n--- Interview Finished ---\n")

    # Safely access final report
    final_report = final_state.get("final_report", {})
    print("✅ Final Report:")
    print(final_report)


if __name__ == "__main__":
    run_interview()

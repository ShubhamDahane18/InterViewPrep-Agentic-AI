from evaluation_graph import build_evaluation_graph
from state import EvaluationState

def main():
    initial_state: EvaluationState = {
        "candidate_name": "John Doe",
        "candidate_email": "john.doe@example.com",
        "company_name": "TechCorp",
        "rounds": [
            {
                "round_name": "Tech",
                "qa": [
                    {"question": "What is polymorphism in OOP?", "answer": "It allows one interface to be used for different types of objects."},
                    {"question": "Explain Python's GIL.", "answer": "It prevents multiple native threads from executing Python bytecodes at once."}
                ]
            },
            {
                "round_name": "HR",
                "qa": [
                    {"question": "Why do you want to join our company?", "answer": "Because I admire your culture of innovation."}
                ]
            }
        ]
    }

    workflow = build_evaluation_graph()
    final_state = workflow.invoke(initial_state)

    print("\n=== Final Report ===")
    print(final_state["final_report"])

if __name__ == "__main__":
    main()

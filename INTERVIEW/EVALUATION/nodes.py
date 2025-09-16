from config import evaluator_llm , llm ,resource_llm
from state import EvaluationState
from schema import RoundEvaluation, Summary, FinalReport, ResourceItem
from datetime import date


# --- Evaluation Node ---
def evaluation_node(state: EvaluationState) -> EvaluationState:
    evaluations = {}

    for round_data in state.get("rounds", []):
        round_name = round_data["round_name"].lower()
        qa_pairs = round_data["qa"]
        qa_text = "\n".join([f"Q: {qa['question']}\nA: {qa['answer']}" for qa in qa_pairs])

        structured_eval_llm = evaluator_llm.with_structured_output(RoundEvaluation)
        try:
            eval_result = structured_eval_llm.invoke(
                f"Evaluate the following {round_name} interview responses:\n\n{qa_text}\n\n"
                "Provide a score (0–10), feedback, reasoning, strengths, weaknesses, suggestions, and examples."
            )
            evaluations[round_name] = eval_result.dict()
        except Exception as e:
            print(f"⚠️ Evaluation for {round_name} failed: {e}")
            evaluations[round_name] = {
                "score": 0,
                "feedback": "No evaluation available.",
                "strengths": [],
                "weaknesses": [],
                "suggestions": [],
                "examples": []
            }

    state["evaluation"] = evaluations
    return state


# --- Feedback Node ---
def feedback_node(state: EvaluationState) -> EvaluationState:
    feedbacks = {}
    for round_name, eval_data in state.get("evaluation", {}).items():
        feedbacks[round_name] = llm.invoke(
            f"Convert the following evaluation into constructive interview feedback for the candidate:\n\n{eval_data}"
        ).content
    state["feedback"] = feedbacks
    return state


# --- Resource Node ---
def resource_node(state: EvaluationState) -> EvaluationState:
    resources = {}
    for round_name, eval_data in state.get("evaluation", {}).items():
        weaknesses = eval_data.get("weaknesses", [])
        if weaknesses:
            res_list = []
            for w in weaknesses:
                suggestion = resource_llm.invoke(
                    f"Suggest one learning resource (book, course, or tutorial) to improve on this weakness:\n{w}"
                ).content
                res_list.append(ResourceItem(name=suggestion))
            resources[round_name] = res_list
    state["resources"] = resources
    return state


# --- Summary Node ---
def summary_node(state: EvaluationState) -> EvaluationState:
    all_strengths, all_weaknesses = [], []
    for eval_data in state.get("evaluation", {}).values():
        all_strengths.extend(eval_data.get("strengths", []))
        all_weaknesses.extend(eval_data.get("weaknesses", []))

    structured_summary_llm = evaluator_llm.with_structured_output(Summary)
    summary = structured_summary_llm.invoke(
        f"Summarize the candidate’s performance. Strengths: {all_strengths}. Weaknesses: {all_weaknesses}."
    )
    state["summary"] = summary.dict()
    return state


# --- Final Report Node ---
def final_report_node(state: EvaluationState) -> EvaluationState:
    candidate_info = {
        "name": state.get("candidate_name", "N/A"),
        "email": state.get("candidate_email", "N/A"),
        "company": state.get("company_name", "N/A"),
        "interview_date": str(date.today())
    }

    final_report = FinalReport(
        candidate=candidate_info,
        evaluation=state.get("evaluation", {}),
        feedback=state.get("feedback", {}),
        resources=state.get("resources", {}),
        summary=state.get("summary", {})
    )
    state["final_report"] = final_report.dict()
    return state

from state import EvaluationState
from schema import FullEvaluation, RoundEvaluation
from utils import present_to_user, clean_json
from datetime import datetime
import json

# Replace with your actual LLM instances
from config import evaluator_llm, resource_llm , llm

def evaluation_node(state: EvaluationState) -> EvaluationState:
    """
    Evaluate all rounds present in state['rounds'] using structured LLM output.
    """
    structured_eval_llm = llm.with_structured_output(schema=FullEvaluation)
    state.setdefault("evaluation", {})

    for round_data in state.get("rounds", []):
        round_name = round_data["round_name"].lower()
        qa_text = "\n".join([f"Q: {qa['question']}\nA: {qa['answer']}" for qa in round_data.get("qa", [])])
        prompt = f"""You are an expert recruiter and career coach. Evaluate the candidate for {state.get('company_name','Unknown')}.

        Candidate Info:
        - Name: state.get('candidate_name','XYZ')
        - Email: state.get('candidate_email','--')

        Rounds Q&A:
        {qa_text}

        For each round (Tech, Project, HR), provide the following in a JSON object:
        1. Score (0.0–10.0)
        2. Concise feedback
        3. Detailed reasoning behind the score
        4. List of strengths (explain why each is a strength)
        5. List of weaknesses (explain why each is a weakness)
        6. Actionable suggestions for improvement
        7. Any relevant examples or references that can help the candidate

        Return ONLY valid JSON.

        """
        try:
            eval_result = structured_eval_llm.invoke(prompt)
            # Some rounds may be missing in the structured output → use .get(round_name, None)
            round_eval = eval_result.model_dump().get(round_name)
            state["evaluation"][round_name] = round_eval
        except Exception as e:
            present_to_user(f"⚠️ Evaluation failed for {round_name}: {e}")
            state["evaluation"][round_name] = None

    return state

def feedback_node(state: EvaluationState) -> EvaluationState:
    """
    Generate concise feedback for each round present in state['evaluation'].
    """
    state.setdefault("feedback", {})

    for round_name, eval_data in state.get("evaluation", {}).items():
        if eval_data:  # skip None
            prompt = f"""
            You are a career coach. Convert the candidate evaluation into detailed feedback for the candidate for {round_name}.
-           Include strengths, weaknesses, and actionable suggestions.
            - Explain why each strength and weakness matters.
            - Make it constructive and encouraging.
            - Write it in readable paragraphs, not JSON.
            - Use examples wherever possible to clarify points
             Candidate Evaluation:
             {eval_data}
             Return plain text feedback.
            """
            llm_output = llm.invoke(prompt).content
            state["feedback"][round_name] = llm_output.strip()
        else:
            state["feedback"][round_name] = "No evaluation available."

    return state

def resource_node(state: EvaluationState) -> EvaluationState:
    """
    Suggest learning resources based on weaknesses in all rounds.
    """
    state.setdefault("resources", {})
    weaknesses = []

    for eval_data in state.get("evaluation", {}).values():
        if eval_data:
            weaknesses += eval_data.get("weaknesses", [])

    if weaknesses:
        prompt = f"""
        You are a career mentor. The candidate has the following weaknesses:
        {', '.join(weaknesses)}

        For each weakness, suggest 1–3 high-quality resources (books, tutorials, courses) that will help improve.
        Return a JSON object with:
        - keys = weakness
        - values = list of resource objects
          - type: Book / Course / Tutorial
          - title
          - author / platform
          - short description
        """
        try:
            raw = resource_llm.invoke(prompt).content
            state["resources"] = clean_json(raw)
        except Exception as e:
            present_to_user(f"⚠️ Resource generation failed: {e}")
            state["resources"] = {}

    return state

def summary_node(state: EvaluationState) -> EvaluationState:
    """
    Summarize candidate's performance across all rounds using an LLM
    to provide detailed coaching-style insights.
    """
    evaluations = state.get("evaluation", {})
    candidate_name = state.get("candidate_name", "Candidate")
    
    # Aggregate evaluation data
    eval_text = ""
    for round_name, eval_data in evaluations.items():
        if eval_data:
            eval_text += f"\n--- {round_name} Round ---\n"
            eval_text += f"Score: {eval_data.get('score', 'N/A')}\n"
            eval_text += f"Feedback: {eval_data.get('feedback', 'N/A')}\n"
            eval_text += f"Strengths: {eval_data.get('strengths', [])}\n"
            eval_text += f"Weaknesses: {eval_data.get('weaknesses', [])}\n"

    # Create prompt directly
    prompt = f"""
    You are a career coach. Provide a detailed, structured summary of a candidate's interview performance.

    Candidate: {candidate_name}

    Evaluations:{eval_text}

    Generate the summary including:
    1. Strengths (with explanations)
    2. Weaknesses (with explanations)
    3. Actionable coaching tips for improvement
    4. Overall impression
    """

    # Invoke LLM
    summary_text = llm.invoke(prompt).content

    # Save summary in state
    state["summary"] = summary_text

    return state

def final_report_node(state: EvaluationState) -> dict:
    """
    Generates the final report for the candidate.
    Always returns a dictionary (never a string).
    """

    candidate_name = state.get("candidate_name", "Unknown")
    company = state.get("company_name", "Unknown")
    interview_date = datetime.now().strftime("%Y-%m-%d")

    # Collect evaluation data with safe defaults
    eval_data = state.get("evaluation", {})
    tech_eval = eval_data.get("tech") or {"score": 0.0, "feedback": "", "strengths": [], "weaknesses": []}
    project_eval = eval_data.get("project") or {"score": 0.0, "feedback": "", "strengths": [], "weaknesses": []}

    # Aggregate strengths and weaknesses
    strengths = (tech_eval.get("strengths") or []) + (project_eval.get("strengths") or [])
    weaknesses = (tech_eval.get("weaknesses") or []) + (project_eval.get("weaknesses") or [])

    # Optionally include resources if present
    resources = state.get("resources", {})

    # Compose the final report
    report = {
        "candidate": {
            "name": candidate_name,
            "email": state.get("candidate_email", "N/A"),
            "company": company,
            "interview_date": interview_date
        },
        "evaluation": {
            "tech": tech_eval,
            "project": project_eval
        },
        "strengths": strengths,
        "weaknesses": weaknesses,
        "resources": resources,
        "summary": state.get("summary", "")
    }

    return {"final_report": report}



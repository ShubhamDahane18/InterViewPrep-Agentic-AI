# nodes.py
from state import TechRoundState
from io_utils import get_user_response, present_to_user
from schema import QAEntry, FullEvaluation , ResourceSuggestions
from config import llm, evaluator_llm , resource_llm
from export_utils import export_state
from datetime import datetime
import json
import random


def maybe_llm_follow_up(question: str, answer: str, round_type: str, state: dict, llm) -> str | None:
    """Use LLM to generate follow-up (capped at 2 per round)."""
    used = state.get("followups_used", {}).get(round_type, 0)
    if used >= 2:
        return None

    if len(answer.split()) > 100 and random.random() < 0.4:
        structured_llm = llm.with_structured_output(QAEntry)
        follow_up = structured_llm.invoke(f"""
        You are a technical interviewer at {state['company_name']}.

        The candidate was asked the following question:
        
        Q: {question}
        
        The candidate gave this long/detailed answer:
        {answer}

        Your task:
        - Dont ask same question.
        - Ask ONE short, precise follow-up question to probe deeper into the same topic.
        - Do not include any explanation or commentary.
        - Return only the follow-up question text.

        """)
        return follow_up.question

    return None

def generate_qa_node(state: TechRoundState, round_type: str) -> dict:
    company = state["company_name"]
    per_topic = state.get("questions_per_topic", 2)
    max_total = state.get("max_questions_per_topic", 5)
    qa_counts = state.get("qa_counts", {}).copy()

    if round_type == "core":
        qa_list = state["core_qa"]
        subjects = state["core_subjects"]
        needing = [s for s in subjects if qa_counts.get(s, 0) < per_topic]
        if needing:
            topic = needing[0]
        else:
            if state.get("decision", {}).get("core") == "continue":
                candidates = [s for s in subjects if qa_counts.get(s, 0) < max_total]
                if not candidates:
                    present_to_user("⚠️ All core subjects reached max questions. Moving on.")
                    return {}
                topic = min(candidates, key=lambda s: qa_counts.get(s, 0))
            else:
                return {}
        prompt_topic = f"core computer science subject: {topic}"

    else:  # tech round
        qa_list = state["tech_qa"]
        all_skills = [skill for cat in state["skills"].values() for skill in cat]
        needing = [s for s in all_skills if qa_counts.get(s, 0) < per_topic]
        if needing:
            topic = needing[0]
        else:
            if state.get("decision", {}).get("technical") == "continue":
                candidates = [s for s in all_skills if qa_counts.get(s, 0) < max_total]
                if not candidates:
                    present_to_user("⚠️ All technical skills reached max questions. Moving on.")
                    return {}
                topic = min(candidates, key=lambda s: qa_counts.get(s, 0))
            else:
                return {}
        prompt_topic = f"technical skill: {topic}"

    structured_llm = llm.with_structured_output(QAEntry)
    qa = structured_llm.invoke(f"""
    You are a technical interviewer for {company}.
    Generate ONE new, unique interview question about the following {prompt_topic}.
    """)

    present_to_user(f"\n[{round_type.capitalize()} - {topic}] Q: {qa.question}")
    answer = get_user_response("Your Answer: ")

     # After main Q&A
    updated_qa_list = qa_list + [{"question": qa.question, "answer": answer}]
    qa_counts[topic] = qa_counts.get(topic, 0) + 1
    
    # Follow-up (if triggered)
    follow_up = maybe_llm_follow_up(qa.question, answer, round_type, state, llm)
    if follow_up:
        present_to_user(f"💬 Interviewer: {follow_up}")
        extra = get_user_response("Your Answer: ")
    
        updated_qa_list.append({"question": follow_up, "answer": extra})
    
        # update follow-up counter
        followups_used = state.get("followups_used", {}).copy()
        followups_used[round_type] = followups_used.get(round_type, 0) + 1
        state["followups_used"] = followups_used

    if round_type == "core":
        return {"core_qa": updated_qa_list, "qa_counts": qa_counts}
    else:
        return {"tech_qa": updated_qa_list, "qa_counts": qa_counts}
    

def core_decision_node(state: TechRoundState) -> dict:
    present_to_user("\n✅ Finished baseline core questions.")
    while True:
        user_input = get_user_response(
            "1) Continue with more Core questions\n2) Move to Technical\nChoose (1/2): "
        ).strip().lower()
        if user_input in {"1", "continue", "c"}:
            action = "continue"; break
        if user_input in {"2", "next", "n"}:
            action = "next"; break
        present_to_user("❌ Invalid input, please type 1 or 2.")

    decision = state.get("decision", {}).copy()
    decision["core"] = action
    return {"decision": decision}


def tech_decision_node(state: TechRoundState) -> dict:
    present_to_user("\n✅ Finished baseline technical questions.")
    while True:
        user_input = get_user_response(
            "1) Continue with more Technical questions\n2) Move to Evaluation\nChoose (1/2): "
        ).strip().lower()
        if user_input in {"1", "continue", "c"}:
            action = "continue"; break
        if user_input in {"2", "next", "n"}:
            action = "next"; break
        present_to_user("❌ Invalid input, please type 1 or 2.")

    decision = state.get("decision", {}).copy()
    decision["technical"] = action
    return {"decision": decision}


def evaluation_node(state: TechRoundState) -> dict:
    present_to_user("\n⚙️ Evaluating performance...")
    structured_eval_llm = evaluator_llm.with_structured_output(FullEvaluation)

    core_text = "\n".join([f"Q: {qa['question']}\nA: {qa['answer']}" for qa in state["core_qa"]])
    tech_text = "\n".join([f"Q: {qa['question']}\nA: {qa['answer']}" for qa in state["tech_qa"]])

    prompt = f"""
    As a senior hiring manager at {state['company_name']}, evaluate the candidate.

    For both Core and Technical sections, provide:
    - A score (0.0–10.0)
    - Concise feedback
    - A list of strengths
    - A list of weaknesses

    **Core Q&A:**
    {core_text}

    **Technical Q&A:**
    {tech_text}
    """

    full_eval = structured_eval_llm.invoke(prompt)

    return {
        "evaluation": full_eval.model_dump()
    }

        
def summary_node(state: TechRoundState) -> dict:
    prompt = (
        f"Summarize the candidate's interview performance for {state['company_name']}.\n"
        f"Core Evaluation: {state['evaluation'].get('core')}\n"
        f"Technical Evaluation: {state['evaluation'].get('technical')}\n"
        f"Provide strengths, weaknesses, and overall impression."
    )
    summary_text = evaluator_llm.invoke(prompt).content
    present_to_user("\n📊 Final Summary:\n" + summary_text)
    filepath = export_state(state)
    present_to_user(f"\n📝 Interview log saved at: {filepath}")
    return {"summary": summary_text}

def final_report_node(state: TechRoundState) -> dict:
    candidate_name = state.get("candidate_name", "Unknown")
    company = state.get("company_name", "Unknown")
    interview_date = datetime.now().strftime("%Y-%m-%d")

    # Collect strengths and weaknesses from evaluation
    eval_data = state.get("evaluation", {})
    core_eval = eval_data.get("core", {})
    tech_eval = eval_data.get("technical", {})

    strengths = core_eval.get("strengths", []) + tech_eval.get("strengths", [])
    weaknesses = core_eval.get("weaknesses", []) + tech_eval.get("weaknesses", [])

    # Generate resource suggestions (if weaknesses exist)
    resources = {}
    if weaknesses:
        structured_llm = resource_llm  # keep raw for text output
        prompt = f"""
        You are a career coach. The candidate showed weaknesses in:
        {', '.join(weaknesses)}.

        Suggest 1–2 high-quality resources (books, tutorials, or courses) for each subject.

        Return ONLY a valid JSON object.
        Keys = subject/skill names.
        Values = lists of resource strings.
        """

        raw_response = structured_llm.invoke(prompt).content
        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1]
            if cleaned.startswith("json"):
                cleaned = cleaned[len("json"):].strip()
            cleaned = cleaned.strip("`").strip()

        try:
            parsed = json.loads(cleaned)
            suggestions = ResourceSuggestions(resources=parsed)
            resources = suggestions.resources
        except Exception as e:
            present_to_user(f"⚠️ Resource generation failed: {e}")
            resources = {}

    # Final report JSON
    report = {
        "candidate": {
            "name": candidate_name,
            "email": state.get("candidate_email", "N/A"),
            "interview_date": interview_date,
            "company": company
        },
        "core": core_eval,
        "technical": tech_eval,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "overall": {
            "score": (
                (core_eval.get("score", 0.0) + tech_eval.get("score", 0.0)) / 2
            ) if eval_data else None,
            "summary": state.get("summary", "")
        },
        "resources": resources
    }

    # Show to candidate / console
    present_to_user("\n📊 Final Report (JSON):")
    present_to_user(json.dumps(report, indent=2))

    # Save to file
    with open("final_report.json", "w") as f:
        json.dump(report, f, indent=2)

    return {"final_report": report}


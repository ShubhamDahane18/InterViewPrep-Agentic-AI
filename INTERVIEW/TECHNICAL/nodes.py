from INTERVIEW.TECHNICAL.state import TechRoundState
from INTERVIEW.TECHNICAL.io_utils import get_user_response, present_to_user
from INTERVIEW.TECHNICAL.schema import QAEntry
from INTERVIEW.TECHNICAL.config import llm
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
        The candidate was asked:
        Q: {question}
        Candidate's answer:
        {answer}
        Your task: ask ONE short follow-up question on same topic.
        """)
        return follow_up.question

    return None

def generate_qa_node(state: TechRoundState, round_type: str) -> dict:
    """Generate one QA for core or tech round (JD-aligned for tech)."""
    company = state["company_name"]
    per_topic = state.get("questions_per_topic", 2)
    qa_counts = state.get("qa_counts", {}).copy()

    if round_type == "core":
        qa_list = state["core_qa"]
        subjects = state["core_subjects"]
        needing = [s for s in subjects if qa_counts.get(s, 0) < per_topic]
        if not needing:
            present_to_user("⚠️ All core subjects reached max questions. Moving on.")
            return {}
        topic = needing[0]
        prompt_topic = f"core computer science subject: {topic}"

    else:  # tech
        qa_list = state["tech_qa"]
        jd_skills = state.get("job_info", {}).get("required_skills", [])
        all_skills = [skill for cat in state["skills"].values() for skill in cat]

        needing = [s for s in jd_skills if s in all_skills and qa_counts.get(s, 0) < per_topic]
        if not needing:
            needing = [s for s in all_skills if qa_counts.get(s, 0) < per_topic]
        if not needing:
            present_to_user("⚠️ All technical skills reached max questions. Moving on.")
            return {}
        topic = needing[0]
        prompt_topic = f"technical skill: {topic}"

    structured_llm = llm.with_structured_output(QAEntry)
    qa = structured_llm.invoke(f"""
    You are a technical interviewer for {company}.
    Generate ONE new, unique interview question about the following {prompt_topic}.
    """)

    present_to_user(f"\n[{round_type.capitalize()} - {topic}] Q: {qa.question}")
    answer = get_user_response("Your Answer: ")

    updated_qa_list = qa_list + [{"question": qa.question, "answer": answer}]
    qa_counts[topic] = qa_counts.get(topic, 0) + 1

    follow_up = maybe_llm_follow_up(qa.question, answer, round_type, state, llm)
    if follow_up:
        present_to_user(f"💬 Interviewer: {follow_up}")
        extra = get_user_response("Your Answer: ")
        updated_qa_list.append({"question": follow_up, "answer": extra})
        state["followups_used"][round_type] += 1

    return {"core_qa": updated_qa_list, "qa_counts": qa_counts} if round_type == "core" else {"tech_qa": updated_qa_list, "qa_counts": qa_counts}

def core_decision_node(state: TechRoundState) -> dict:
    present_to_user("\n✅ Finished baseline core questions.")
    while True:
        user_input = get_user_response("1) Continue core questions\n2) Move to Technical\nChoose (1/2): ").strip().lower()
        if user_input in {"1", "continue", "c"}:
            action = "continue"; break
        if user_input in {"2", "next", "n"}:
            action = "next"; break
        present_to_user("❌ Invalid input, please type 1 or 2.")
    state["decision"]["core"] = action
    return {"decision": state["decision"]}

def tech_decision_node(state: TechRoundState) -> dict:
    present_to_user("\n✅ Finished baseline technical questions.")
    while True:
        user_input = get_user_response("1) Continue technical questions\n2) Finish Tech Round\nChoose (1/2): ").strip().lower()
        if user_input in {"1", "continue", "c"}:
            action = "continue"; break
        if user_input in {"2", "finish", "f", "n", "next"}:
            action = "finish"; break
        present_to_user("❌ Invalid input, please type 1 or 2.")
    state["decision"]["technical"] = action
    return {"decision": state["decision"]}

from langchain.prompts import ChatPromptTemplate

# -----------------------------
# HR Question Prompt (with Past Interaction Handling)
# -----------------------------
tech_question_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a professional **HR interviewer** conducting a structured interview.  

### Your Role
- Act as a polite, empathetic, and professional HR interviewer.  
- Guide the candidate through a realistic HR interview flow.  
- Ask competency-based, behavioral, or situational questions when relevant.  
- Always align your questions with the **job description (JD)** and the **candidate’s resume**.  
- NEVER answer as the candidate — only ask questions.  

### Interviewing Guidelines
1. Ask **exactly ONE question** at a time.  
2. You may either:  
   - Ask a **new question** (to progress the section), OR  
   - Ask a **follow-up question** to the candidate’s most recent answer (if clarification or depth is needed).  
3. Keep every question **short, clear, and natural**.  
4. Do NOT repeat or rephrase previous questions unless it’s a follow-up.  
5. Adapt tone & style based on the current section:  
   - **interviewer_intro** → Warm greeting, confirm readiness.  
   - **intro** → Icebreaker, light conversation, build comfort.  
   - **personal_fit** → Motivation, teamwork, adaptability, career goals.  
   - **behavioral** → STAR method style: “Tell me about a time when…” with probing follow-ups.  
   - **role_fit** → Skills, role alignment, applied experiences.  
   - **end** → Wrap up politely, thank the candidate, and guide next steps.  
6. Always maintain **professional HR etiquette**: neutral, unbiased, encouraging.  
"""),
    ("human", """
### Candidate Context
- **Resume Highlights**: {resume_info}  
- **Job Description (JD)**: {jd_info}  
- **Current Section**: {section_name}  

### Past Interaction
- The following is a chronological list of recent Q&A in this section (most recent first).  
- It may also be **empty** if no questions have been asked yet in this section.  
{prev_qas}  

### Task
Ask **one interview question** for the current section: {section_name}.  
👉 You may choose to ask a **new question** OR a **follow-up question** on the most recent Q&A if it helps evaluate the candidate better.  
Ensure the question is natural, contextual, and avoids unnecessary repetition.  
""")
])



from INTERVIEW.util import load_llm
from INTERVIEW.TECHNICAL.state import TechRoundState

def format_prev_qas(qas: list[dict]) -> str:
    if not qas:
        return "None"
    return "\n".join(
        f"Q: {qa['question']}\nA: {qa['answer'] or '(not answered yet)'}"
        for qa in qas
    )

def tech_round_node(state: TechRoundState) -> TechRoundState:
    """Generate next HR interview question for the current round."""

    # Get context: previous Q/A in this round
    prev_qas = state.questions_answers.get(state.section_name, [])

    prompt = tech_question_prompt.format_messages(
        resume_info=state.resume_info,
        jd_info=state.jd_info,
        section_name=state.section_name,
        prev_qas=format_prev_qas(prev_qas)
    )

    llm = load_llm()
    response = llm.invoke(prompt)
    question = response.content.strip()
    if state.section_name == "interviewer_intro":
        return {"response":question , "get_user_intent":True}
    return {"response":question , "is_qa":True , "get_user_intent": False}
    






























# from INTERVIEW.TECHNICAL.state import TechRoundState
# from INTERVIEW.TECHNICAL.io_utils import get_user_response, present_to_user
# from INTERVIEW.TECHNICAL.schema import QAEntry
# from INTERVIEW.TECHNICAL.config import llm
# import random


# def maybe_llm_follow_up(question: str, answer: str, round_type: str, state: TechRoundState, llm) -> dict | None:
#     """Generate a follow-up question if appropriate and store it in state."""
#     used = state.get("followups_used", {}).get(round_type, 0)
#     if used >= 2:
#         return None

#     if len(answer.split()) > 100 and random.random() < 0.5:
#         structured_llm = llm.with_structured_output(QAEntry)
#         follow_up = structured_llm.invoke(f"""
#         You are a senior technical interviewer at {state['company_name']}.
#         Candidate: {state['candidate_name']}
#         Previous Q: {question}
#         Candidate A: {answer}

#         Ask ONE concise follow-up question naturally, like a real interview. Do not give answers.
#         """)
#         return {"question": follow_up.question, "round_type": round_type}
#     return None


# def generate_qa_node(state: TechRoundState, round_type: str) -> dict:
#     """Generate one QA pair and store all interactions in state for frontend."""
#     company = state["company_name"]
#     per_topic = state.get("questions_per_topic", 2)
#     qa_counts = state.get("qa_counts", {}).copy()

#     # Determine topic or skill
#     if round_type == "core":
#         qa_list = state.get("core_qa", [])
#         subjects = state.get("core_subjects", [])
#         needing = [s for s in subjects if qa_counts.get(s, 0) < per_topic]
#         if not needing:
#             state["response"] = "⚠️ All core subjects covered. Moving on."
#             state["user_input"] = None
#             return {"state": state}
#         topic = needing[0]
#         prompt_topic = f"core computer science topic: {topic}"
#     else:
#         qa_list = state.get("tech_qa", [])
#         jd_skills = state.get("job_info", {}).get("required_skills", [])
#         all_skills = [skill for cat in state.get("skills", {}).values() for skill in cat]
#         needing = [s for s in jd_skills if s in all_skills and qa_counts.get(s, 0) < per_topic]
#         if not needing:
#             needing = [s for s in all_skills if qa_counts.get(s, 0) < per_topic]
#         if not needing:
#             state["response"] = "⚠️ All technical skills covered. Moving on."
#             state["user_input"] = None
#             return {"state": state}
#         topic = needing[0]
#         prompt_topic = f"technical skill: {topic}"

#     # Generate main question using LLM
#     structured_llm = llm.with_structured_output(QAEntry)
#     qa = structured_llm.invoke(f"""
#         You are a professional technical interviewer at {company}.
#         Generate ONE realistic, concise interview question about: {prompt_topic}.
#         Address the candidate {state['candidate_name']} naturally.
#         """)

#     # Update state for frontend
#     state["response"] = qa.question
#     state["user_input"] = None

#     # Capture candidate input
#     answer = get_user_response("Your Answer: ")
#     state["user_input"] = answer

#     # Update QA list
#     updated_qa_list = qa_list + [{"question": qa.question, "answer": answer}]
#     qa_counts[topic] = qa_counts.get(topic, 0) + 1

#     # Possibly generate follow-up
#     follow_up_info = maybe_llm_follow_up(qa.question, answer, round_type, state, llm)
#     if follow_up_info:
#         state["response"] = follow_up_info["question"]
#         state["user_input"] = None

#         extra = get_user_response("Your Answer: ")
#         state["user_input"] = extra

#         updated_qa_list.append({"question": follow_up_info["question"], "answer": extra})
#         state.setdefault("followups_used", {}).setdefault(round_type, 0)
#         state["followups_used"][round_type] += 1

#     # Update state fully
#     if round_type == "core":
#         state["core_qa"] = updated_qa_list
#     else:
#         state["tech_qa"] = updated_qa_list
#     state["qa_counts"] = qa_counts

#     return {"state": state}


# def core_decision_node(state: TechRoundState) -> dict:
#     """Frontend-friendly core round decision node."""
#     state["response"] = "✅ Finished baseline core questions."
#     state["user_input"] = None

#     while True:
#         user_input = get_user_response("1) Continue core questions\n2) Move to Technical\nChoose (1/2): ").strip().lower()
#         state["user_input"] = user_input

#         if user_input in {"1", "continue", "c"}:
#             action = "continue"
#             break
#         if user_input in {"2", "next", "n"}:
#             action = "next"
#             break
#         state["response"] = "❌ Invalid input, please type 1 or 2."
#         state["user_input"] = None

#     state.setdefault("decision", {})["core"] = action
#     return {"state": state}


# def tech_decision_node(state: TechRoundState) -> dict:
#     """Frontend-friendly technical round decision node."""
#     state["response"] = "✅ Finished baseline technical questions."
#     state["user_input"] = None

#     while True:
#         user_input = get_user_response("1) Continue technical questions\n2) Finish Tech Round\nChoose (1/2): ").strip().lower()
#         state["user_input"] = user_input

#         if user_input in {"1", "continue", "c"}:
#             action = "continue"
#             break
#         if user_input in {"2", "finish", "f", "n", "next"}:
#             action = "finish"
#             break
#         state["response"] = "❌ Invalid input, please type 1 or 2."
#         state["user_input"] = None

#     state.setdefault("decision", {})["technical"] = action
#     return {"state": state}



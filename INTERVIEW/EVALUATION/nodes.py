from INTERVIEW.util import load_llm
from INTERVIEW.EVALUATION.utils import qa_to_str
from INTERVIEW.EVALUATION.state import EvaluationState
from INTERVIEW.EVALUATION.schema import RoundEvaluation
from datetime import date
from langchain.prompts import ChatPromptTemplate


evaluation_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an experienced interviewer evaluating a candidate's performance in an interview round.

Your job is to:
1. Analyze the candidate's Q&A transcript for the given round.
2. Provide a fair and constructive evaluation.
3. Return a structured output strictly following the RoundEvaluation schema.

### Rules:
- score → A number between 0 and 10 (0 = very poor, 10 = excellent).
- reasoning → Brief explanation of why this score was assigned.
- strengths → Key areas where the candidate performed well (list).
- weaknesses → Areas where the candidate struggled or gave incomplete answers (list).
- suggestions → Clear, actionable steps for improvement (list).
- examples → Specific excerpts or references from candidate responses that justify the evaluation (list).
- Do not invent details outside the transcript.
- Be objective, concise, and constructive.

### Output Schema: RoundEvaluation
- score: float (0–10)
- reasoning: str
- strengths: List[str]
- weaknesses: List[str]
- suggestions: List[str]
- examples: List[str]
"""),
    ("human", """
Round name: {round_name}
Q&A Transcript:
{qa_text}
""")
])

# --- Evaluation Node ---
def evaluation_node(state: EvaluationState) -> EvaluationState:

    # LLM with structured output
    llm = load_llm()
    llm_ws = llm.with_structured_output(RoundEvaluation)

    # Chain
    chain = evaluation_prompt | llm_ws

    # Invoke
    result: RoundEvaluation = chain.invoke({
        "round_name": state.get("round_name", ""),
        "qa_text": qa_to_str(state["questions_answers"]),
    })

    # Update state
    return {"evaluation":result.model_dump()}


# --- Summary Node ---
summary_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an interviewer assistant. 
Create a concise, professional summary of the candidate's performance based on the evaluation and job description.

Instructions:
- Use the evaluation (score, reasoning, strengths, weaknesses, suggestions, examples) and JD.
- Align feedback with the role requirements.
- Be polite, constructive, and encouraging.
- Keep it 3–5 sentences.
- Return only the summary text (no extra formatting or JSON).
"""),
    ("human", """
Round: {round_name}

Job Description:
{jd_info}

Evaluation:
{evaluation}
""")
])

from langchain_core.output_parsers import StrOutputParser

def summary_node(state) -> dict:
    """
    Generate a concise, professional summary of the candidate's performance
    based on evaluation and JD, and update the state.
    """
    llm = load_llm()
    chain = summary_prompt | llm | StrOutputParser()

    result = chain.invoke({
        "round_name": state.get("round_name", ""),
        "jd_info": state.get("jd_info"),
        "evaluation": state.get("evaluation"),
    })

    return {'summary':result}


# --- Final Report Node ---
final_report_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an interviewer assistant. 
Your job is to create a polished, professional final report for a candidate.

Instructions:
- Use the candidate's name, the evaluation results, and the summary.
- Format the report with clear headings and sections.
- Include:
    1. Candidate Name
    2. Round Name
    3. Evaluation Highlights
    4. Summary
- Tone: professional, constructive, and encouraging.
- Use proper formatting for readability (headings, bullet points where applicable).
- Return only the report text.
"""),
    ("human", """
Candidate Name: {candidate_name}
Round: {round_name}

Evaluation:
{evaluation}

Summary:
{summary}
""")
])

# -------------------------------
# Final report node
# -------------------------------
def final_report_node(state) -> dict:
    """
    Generate a polished final report for the candidate including evaluation, summary, and candidate name.
    """
    llm = load_llm()

    chain = final_report_prompt | llm | StrOutputParser()


    result = chain.invoke({
        "candidate_name": state.get("candidate_name"),
        "round_name": state.get("round_name", ""),
        "evaluation": state.get("evaluation"),
        "summary": state.get("summary"),
    })

    
    return {'final_report':result}

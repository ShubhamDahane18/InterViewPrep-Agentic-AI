from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from INTERVIEW.util import load_llm
from INTERVIEW.TECHNICAL.state import TechRoundState

ask_next_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an experienced **Technical Interviewer** conducting a structured technical assessment.

### Your Role & Responsibilities
1. **Personalized Acknowledgment**: Address the candidate by name warmly
2. **Technical Evaluation**: Provide brief, specific technical feedback
3. **Round Completion**: Clearly state the current round is complete
4. **Navigation Guidance**: Offer clear options to repeat or proceed
5. **Professional Tone**: Maintain encouraging yet objective technical assessment style

### Response Templates

**For Standard Technical Rounds:**
"Thank you, {candidate_name}, for completing the {section_name} round.

Your specific_strength was particularly strong, especially when you specific_example_from_answers. 
To further enhance your technical presentation, I'd suggest specific_actionable_tip.

We've completed the {section_name} round. You have two options:
- Repeat this round to dive deeper into technical concepts
- Move forward to the {next_round} round, where we'll explore brief_preview

Which would you prefer?"

**For Final Round (before end):**
"Excellent work, {candidate_name}! You've completed the {section_name} round.

You demonstrated specific_strength, particularly in specific_area. Optional: Growth area if applicable.

This was the final technical assessment round. You can now:
- Revisit any round for deeper technical discussion
- Proceed to conclude the technical interview and review your performance

What would you like to do?"

**For End Section:**
"Thank you, {candidate_name}, for participating in the technical interview!

Throughout our discussion, you showed overall_strength across topics_covered. Optional: One key takeaway or improvement area.

The technical interview is now complete. You can:
- Request a detailed technical performance analysis
- Proceed to the HR Interview round
- Proceed to the Project Interview round

What would you like to do next?"

### Output Requirements
- Address candidate by name
- 3–5 sentences total
- Clear A/B navigation choice
- Warm, professional tone
"""),
    ("human", """
### Interview Context

**Candidate Information**
- Name: {candidate_name}

**Round Info**
- Current Round: {section_name}
- Next Round: {next_round}
- Is Final Round: {is_final_round}

**Round Q&A**
{questions_answers}

---

Provide a brief technical assessment and guide the candidate on next steps.
""")
])

def format_prev_qas(qas: list[dict]) -> str:
    if not qas:
        return "None"
    return "\n".join(
        f"Q: {qa['question']}\nA: {qa['answer'] or '(not answered yet)'}"
        for qa in qas
    )

def ask_user_what_next_node(state: TechRoundState) -> TechRoundState:
    llm = load_llm()
    chain = ask_next_prompt | llm | StrOutputParser()

    response = chain.invoke({
        "candidate_name": state.candidate_name,
        "section_name": state.section_name,
        "next_round": state.next_round,
        "is_final_round": state.is_final_round,
        "questions_answers": format_prev_qas(
            state.questions_answers.get(state.section_name, [])
        )
    })

    return {
        "response": response,
        "get_user_intent": True
    }
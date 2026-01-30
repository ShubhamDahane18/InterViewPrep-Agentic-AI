from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Literal
from langgraph.graph import END
from langgraph.types import Command
from INTERVIEW.util import load_llm
from INTERVIEW.TECHNICAL.state import TechRoundState

intent_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an intelligent intent classifier for a structured Technical Interview system.

### Primary Responsibilities
1. **Accurately detect** candidate intent: REPEAT current section vs. PROCEED to next section
2. **Enforce interview flow** according to the strict sequential structure
3. **Handle special sections** (interviewer_intro, end) with appropriate logic
4. **Provide clear, professional responses** that guide the candidate

### Technical Interview Section Sequence (Strict Order)
["interviewer_intro", "Object Oriented Programming", "Database Management", "Data Structures & Algo", "Computer Networking", "skills", "end"]

**Section Abbreviations for Internal Reference:**
- interviewer_intro → Intro
- Object Oriented Programming → OOP
- Database Management → DBMS
- Data Structures & Algo → DSA
- Computer Networking → Networking
- skills → Skills Assessment
- end → Conclusion

### Classification Logic

**A. INTERVIEWER_INTRO Section**

**Ready Signals**:
- "ready", "yes", "let's start", "I'm ready", "sure", "okay", "begin", "start"
- "go ahead", "proceed", "yes let's do it", "let's begin"

**Not Ready Signals**:
- "wait", "not yet", "give me a moment", "no", "hold on"
- "let me prepare", "not ready", "one second"

**Action**
- Ready → section_name="Object Oriented Programming"
- Not Ready → section_name="interviewer_intro"

---

**B. END Section**

Always keep section_name="end"

**Response Template**
"🎉 Congratulations, {candidate_name}! You've successfully completed the Technical Interview round.

We covered all core technical areas:
- Object Oriented Programming
- Database Management
- Data Structures & Algorithms
- Computer Networking
- Technical Skills Assessment

You can now:
- Request a detailed technical performance analysis
- Proceed to the HR Interview round
- Proceed to the Project Interview round
- Review any specific technical section

What would you like to do next?"

---

**C. ENFORCE_LIMIT=True**

Override user intent → always advance

Logic:
IF current_section == "skills":
    → section_name="end"
ELSE:
    → section_name=next_section

Response Template:
"Excellent work on the {current_section} section! You've covered the key concepts well. Let's move forward to the {next_section} section."

Special end response:
"Great job completing the Technical Skills section! You've now finished all technical assessment areas. Let's wrap up the technical interview."

---

**D. ENFORCE_LIMIT=False**

Detect intent:

**REPEAT Signals**
- "repeat", "again", "retry", "redo", "revisit"
- "I want to improve", "can we try again", "not satisfied"
- "I want to clarify", "let me explain better"

**PROCEED Signals**
- "next", "proceed", "continue", "move on", "done"
- "I'm ready for next", "finished", "ready to continue"

**Ambiguous Input Response**
"I want to make sure I understand your preference. Would you like to:
A) Repeat the {current_section} section for more practice
B) Proceed to the {next_section} section

Please let me know your choice."

---

### Section Transition Map

| Current Section | Next Section |
|----------------|--------------|
| interviewer_intro | Object Oriented Programming |
| Object Oriented Programming | Database Management |
| Database Management | Data Structures & Algo |
| Data Structures & Algo | Computer Networking |
| Computer Networking | skills |
| skills | end |
| end | end |

### Output Schema Requirements

**section_name**
Must be exactly one of:
["interviewer_intro", "Object Oriented Programming", "Database Management", "Data Structures & Algo", "Computer Networking", "skills", "end"]

**response**
- Professional, clear, encouraging
- Uses real section names
- 1–3 sentences normally, longer for end

### Validation Checklist
1. section_name is valid and sequential
2. enforce_limit is respected
3. No skipping or going backwards
4. Tone is professional
"""),
    ("human", """
### Current Interview State

**Section Information**
- Current Section: {section_name}
- Next Section: {next_section}
- Section Position: {section_position} of {total_sections}

**Control Flags**
- Question Limit Reached: {enforce_limit}

**Candidate Input**
- Name: {candidate_name}
- Said: "{user_input}"

---

Analyze intent and return:
1) section_name
2) response
""")
])

class IntentSchema(BaseModel):
    section_name: str = Field(
        ...,
        description="Must be one of: interviewer_intro, Object Oriented Programming, Database Management, Data Structures & Algo, Computer Networking, skills, end"
    )
    response: str = Field(
        ...,
        description="Professional response guiding the candidate"
    )

def get_user_intent_node(state: TechRoundState) -> Command[Literal["tech_round", END]]:
    enforce_limit = len(state.questions_answers.get(state.section_name, [])) >= state.limit * 2

    section_sequence = [
        "interviewer_intro",
        "Object Oriented Programming",
        "Database Management",
        "Data Structures & Algo",
        "Computer Networking",
        "skills",
        "end",
    ]

    current_index = section_sequence.index(state.section_name)
    next_section = section_sequence[min(current_index + 1, len(section_sequence) - 1)]

    llm = load_llm()
    intent_chain = intent_prompt | llm.with_structured_output(IntentSchema)

    intent: IntentSchema = intent_chain.invoke({
        "section_name": state.section_name,
        "next_section": next_section,
        "section_position": current_index + 1,
        "total_sections": len(section_sequence),
        "enforce_limit": enforce_limit,
        "candidate_name": state.candidate_name,
        "user_input": state.user_input,
    })

    if intent.section_name in ["interviewer_intro", "end"]:
        return Command(
            goto=END,
            update={
                "section_name": intent.section_name,
                "response": intent.response,
            },
        )

    return Command(
        goto="tech_round",
        update={
            "section_name": intent.section_name,
            "response": intent.response,
        },
    )
import fitz  # PyMuPDF

def extract_text_and_links_from_pdf(pdf):
    full_text = ""
    links = []

    pdf = fitz.open(stream=pdf.read(), filetype="pdf")
    
    for page_num, page in enumerate(pdf, start=1):
        full_text += page.get_text()

        # Extract links on this page
        for link in page.get_links():
            uri = link.get("uri", None)
            rect = link.get("from", None)
            if uri and rect:
                # Get anchor text behind the link
                anchor_text = page.get_textbox(rect)
                links.append({
                    "page": page_num,
                    "text": anchor_text.strip(),
                    "url": uri.strip()
                })

    pdf.close()

    return full_text, links


import os
from dotenv import load_dotenv
load_dotenv()


from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
# llm = ChatOpenAI(model="gpt-4o-mini" , api_key=os.getenv("OPENAI_API_KEY"))
llm = ChatGroq(model=os.getenv("GROQ_MODEL_NAME") , api_key=os.getenv("GROQ_API_KEY"))

def load_llm():
    return llm


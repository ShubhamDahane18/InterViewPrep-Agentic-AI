# config.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# It's best practice to load your API key from environment variables
# from dotenv import load_dotenv
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Replace this with your actual key or load from environment
GOOGLE_API_KEY = ""

# A fast, cost-effective model for generating questions
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", google_api_key=GOOGLE_API_KEY)

# A more powerful model for high-quality evaluation and summarization
evaluator_llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=GOOGLE_API_KEY)

resource_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GOOGLE_API_KEY)
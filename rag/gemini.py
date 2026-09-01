import os
import time
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env
load_dotenv()

# Configure API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load model only once
model = genai.GenerativeModel("gemini-3.6-flash")


def ask_gemini(context, question):

    prompt = f"""
You are an AI assistant.

Answer ONLY using the context below.

If the answer is not present in the context, say:

"I couldn't find the answer in the uploaded PDF."

Context:

{context}

Question:

{question}

Answer:
"""

    print("Calling Gemini...")

    start = time.time()

    response = model.generate_content(prompt)

    print(f"Gemini took {time.time() - start:.2f} seconds")

    return response.text

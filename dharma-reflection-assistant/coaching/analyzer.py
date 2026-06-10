import ollama

from config import LLM_MODEL
from coaching.prompts import ANALYSIS_PROMPT


def create_search_query(question: str) -> str:
    prompt = f"""
You are a mythology retrieval planner.

Convert this situation into mythological search concepts.

Situation:

{question}

Extract:

- emotions
- ethical tensions
- dharma issues
- karma issues
- leadership issues
- truth
- justice
- forgiveness
- compassion

Return ONLY keywords separated by commas.
"""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


def analyze(
    question: str,
    context: str,
    profile: dict
) -> str:

    prompt = f"""
{ANALYSIS_PROMPT}

USER PROFILE

{profile}

MYTHOLOGICAL CONTEXT

{context}

USER QUESTION

{question}
"""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]
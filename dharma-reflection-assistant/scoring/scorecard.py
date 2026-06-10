import json
import re

import ollama

from config import LLM_MODEL


DEFAULT_SCORES = {
    "dharma": 5,
    "satya": 5,
    "karuna": 5,
    "self_control": 5,
    "responsibility": 5,
    "ego": 5
}


def extract_json(text: str):

    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )

    if not match:
        return None

    return match.group(0)


def normalize_score(value):

    try:
        value = int(value)
        return max(0, min(10, value))
    except Exception:
        return 5


def generate_scorecard(
    question: str,
    context: str
):

    prompt = f"""
You are a Dharma evaluator.

Analyze the user's behavior.

Question:
{question}

Mythological Context:
{context}

Return ONLY valid JSON.

Example:

{{
    "dharma": 7,
    "satya": 6,
    "karuna": 5,
    "self_control": 8,
    "responsibility": 9,
    "ego": 3
}}

Definitions:

dharma:
0 = completely adharmic
10 = strongly aligned with dharma

satya:
0 = dishonest
10 = truthful

karuna:
0 = cruel
10 = compassionate

self_control:
0 = impulsive
10 = disciplined

responsibility:
0 = irresponsible
10 = accountable

ego:
0 = humble
10 = ego-driven

Return JSON only.
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

    raw = response["message"]["content"]

    try:

        json_text = extract_json(raw)

        if not json_text:
            return DEFAULT_SCORES

        data = json.loads(json_text)

        return {
            "dharma":
                normalize_score(
                    data.get("dharma", 5)
                ),
            "satya":
                normalize_score(
                    data.get("satya", 5)
                ),
            "karuna":
                normalize_score(
                    data.get("karuna", 5)
                ),
            "self_control":
                normalize_score(
                    data.get(
                        "self_control",
                        5
                    )
                ),
            "responsibility":
                normalize_score(
                    data.get(
                        "responsibility",
                        5
                    )
                ),
            "ego":
                normalize_score(
                    data.get("ego", 5)
                )
        }

    except Exception:

        return DEFAULT_SCORES
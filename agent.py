# Extract ticket feilds using an LLM, search the knowledge base, ticket is a known or new issue?, suggest the correct next action.

import os
import json
import time
import ollama
from typing import Dict, Any
from kb.search import search_kb

# config
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "false").lower() == "true"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")


def call_llm(prompt: str, max_retries: int = 2, delay: float = 1.0) -> str:
    """
    Calls a local Ollama LLM with retry logic
    """

    if USE_MOCK_LLM:
        return json.dumps({
            "summary": "Mock summary of the ticket.",
            "category": "Bug",
            "severity": "High"
        })

    for attempt in range(max_retries):
        try:
            response = ollama.chat(
                model=OLLAMA_MODEL,
                messages=[{"role": "user", "content": prompt}]
            )
            return response["message"]["content"]
        except Exception as e:
            # retry on errors
            if attempt == max_retries - 1:
                raise RuntimeError(f"LLM failed after retries: {e}")
            time.sleep(delay)

# ticket field extraction (LLM)
def extract_ticket_fields(description: str) -> Dict[str, str]:
    """
    Uses Ollama LLM to classify the ticket into structured fields
    """

    prompt = f"""
            Extract structured metadata from the following support ticket.
            Return ONLY a valid JSON object with keys:
            - summary (1–2 sentence summary)
            - category (Billing, Login, Performance, Bug, Question)
            - severity (Low, Medium, High, Critical)

            Ticket:
            \"\"\"{description}\"\"\"
            """

    raw = call_llm(prompt)

    # try parsing as JSON safely
    try:
        data = json.loads(raw)
    except Exception:
        data = {
            "summary": "N/A",
            "category": "Unknown",
            "severity": "Low"
        }

    return data

# triage orchestration (core agent)
def triage_ticket(description: str) -> Dict[str, Any]:
    """
    Extract ticket fields using LLM -> KB search -> known or new issue -> suggest next action.
    """

    if not description.strip():
        return {
            "error": "Ticket description is empty.",
            "known_issue": False,
            "next_action": "Ask user to provide a proper issue description."
        }

    # extract ticket fields using LLM
    fields = extract_ticket_fields(description)

    # KB search
    kb_matches = search_kb(description, top_k=3)
    best_score = kb_matches[0]["score"] if kb_matches else 0.0
    is_known_issue = best_score > 0.30

    # next action logic
    if is_known_issue:
        next_action = kb_matches[0].get("recommended_action", "Attach KB article and respond to user.")
    else:
        sev = fields.get("severity", "Low")
        if sev in ["High", "Critical"]:
            next_action = "Escalate to engineering team."
        else:
            next_action = "Request more information from the user."

    # response
    return {
        "summary": fields.get("summary"),
        "category": fields.get("category"),
        "severity": fields.get("severity"),
        "known_issue": is_known_issue,
        "best_kb_match": kb_matches[0] if kb_matches else None,
        "kb_matches": kb_matches,
        "next_action": next_action
    }


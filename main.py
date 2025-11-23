#  FastAPI service that exposes the Ticket Triage Agent.
"""
POST /triage
Body: {"description": "..."}
Returns: structured JSON
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import triage_ticket

app = FastAPI(
    title="Vikara Support Ticket Triage Agent API",
    version="1.0.0",
    description="AI powered ticket triage using LLM (Ollama)."
)

# request and response models
class TicketRequest(BaseModel):
    description: str

class TriageResponse(BaseModel):
    summary: str | None
    category: str | None
    severity: str | None
    known_issue: bool
    next_action: str
    best_kb_match: dict | None
    kb_matches: list | None

# routes
@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/triage", response_model=TriageResponse)
def triage(ticket: TicketRequest):
    """
    Accepts a support ticket and returns structured triage results
    """
    try:
        result = triage_ticket(ticket.description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # if error from agent (like empty description, etc.)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result

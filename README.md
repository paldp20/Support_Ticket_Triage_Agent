# Vikara Support Ticket Triage Agent

The Vikara Support Ticket Triage Agent is an AI powered system that automates the triage of customer support tickets.  
It uses **LLMs (via Ollama)** + **semantic embeddings (Sentence Transformers)** to:

- Generate concise ticket summaries  
- Classify category & severity  
- Detect similarity with known issues  
- Recommend next actions  
- Suggest the best matching KB articles  

This repository contains:

- **FastAPI backend**  
- **Streamlit UI**  
- **LLM agent logic (Ollama)**  
- **Automated tests with pytest**  
- **Dockerized backend deployment**

---

# Tech Stack

### Backend
- **FastAPI**: API server  
- **Ollama**: local LLM inference  
- **SentenceTransformers**: embedding generation  
- **scikit-learn**: cosine similarity  
- **Uvicorn**: ASGI server  

### Frontend
- **Streamlit**: minimal UI  

### DevOps
- **Docker**: containerized backend  
- **pytest**: API test suite  

---

# Project Structure

### What Each File Does

| File | Purpose |
|------|---------|
| `main.py` | API server, routes, validation models |
| `agent.py` | LLM pipeline, embeddings, KB similarity search |
| `app.py` | User interface in Streamlit |
| `tests.py` | Automated API testing |
| `kb.json` | Knowledge-base articles |
| `Dockerfile` | Container for FastAPI |
| `requirements.txt` | Python deps |

---

# System Architecture

Streamlit UI (app.py)

|

|  HTTP POST /triage

v

FastAPI (main.py)

|

|  calls

v

Agent (agent.py)

|

|

v

Triage response


---

# Running the Project Locally

## Start Ollama

Install Ollama:  
https://ollama.com/download

Pull your model:

```bash
ollama pull mistral
```

Ensure Ollama is running:

```bash
ollama serve
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Start the FastAPI backend

```bash
uvicorn main:app --reload --port 8000
```

Health check:

```bash
GET http://localhost:8000/health
```

API docs:
http://localhost:8000/docs


## Start streamlit UI

In a new terminal:

```bash
streamlit run app.py
```

Opens at:
http://localhost:8501

## Run tests

In another terminal:

```bash
pytest -v
```

You should see:
5 passed

---

# API Usage

## POST `/triage`

Request:

```bash
{
  "description": "My dashboard keeps crashing when loading widgets."
}
```

Sample response:
```bash
{
  "summary": "Dashboard crashes on widget load",
  "category": "Bug",
  "severity": "High",
  "known_issue": true,
  "next_action": "Restart the analytics worker service and clear widget cache",
  "best_kb_match": 
  {
    "id": "KB-122",
    "category": "Bug",
    "recommended_action": "Clear widget cache and restart analytics service",
    "similarity": 0.89
  },
  "kb_matches": [...]
}
```

---

# Docker deployment (Backend only)

The Dockerfile runs the FastAPI backend.

## Build Image

```bash
docker build -t <folder-name> .
```

## Run container
```bash
docker run -p 8000:8000 <folder-name>
```

The API is now available at:
- http://localhost:8000/triage
- http://localhost:8000/docs

> Note: Ollama must run on the host and be accessible to the container.

---

# Production Deployment

## **Recommended platforms**

- **AWS ECS / Fargate**: scalable container deployment
- **GCP Cloud Run**: serverless containers
- **Azure Container Instances**
- **Docker Compose**: local multi-service deployment

## **Deployment steps**

1. Deploy FastAPI container -> ECS or Cloud Run
2. Run Ollama on a compute node / VM
3. Expose Ollama internally (e.g., TCP 11434)
4. Configure container to call Ollama host
5. Deploy Streamlit either:
    - In a separate container
    - Or in the same VM
6. Add a reverse proxy (NGINX) if needed

---

# Status
- All tests passing
- Backend is stable
- Streamlit UI is connected
- Backend is containerized fully

> Note: VSCode is used for this project by me.



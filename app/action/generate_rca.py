
from langchain_groq import ChatGroq
from app.schemas.incident import Incident, RCAResponse
import getpass
import os
import json
if "LLM_API_KEY" not in os.environ:
    os.environ["LLM_API_KEY"] = getpass.getpass("Enter your Groq API key: ")


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.environ["LLM_API_KEY"],
    temperature=1,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
    # other params...
)
async def generate_rca(incident:Incident, similar_incidents:list[str]) -> RCAResponse:
    similar_text = ("\n".join(f"Historical Incident: {incident}" for incident in similar_incidents) or "No similar incidents found")
    prompt = f"""You are a Senior Cloud Reliability Engineer performing Root Cause Analysis.

##Current Incident

Title: {incident.title}

Service: {incident.service}

Environments: {incident.environment}

Severity: {incident.severity}

Symptons: {incident.symptoms}

## Similar Historical Incidents

{similar_text}

##Task

Analyze the current incident using the similar historical Incidents as context.

Return a JSON object with exactly these fields:
- "root_cause": str = what caused this incident
- "confidence": int = your confidence in this analysis (0-100)
- "recommended_fix": str = how to resolve this incident
- "first_action": str = the immediate step to take
- "recalled_from": list[str] = the historical incidents that informed your analysis (copy relevant fields)

Return ONLY valid JSON. No markdown. No explanation."""
    response = await llm.ainvoke([
        {"role": "user", "content": prompt}
    ])
    raw = response.content
    final_data = json.loads(raw)
    return RCAResponse(**final_data)

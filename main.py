from fastapi import FastAPI
from dotenv import load_dotenv
from openai import OpenAI
import os
import requests
import json

load_dotenv()

app = FastAPI(title="ServiceNow AI CMDB Impact Analyzer")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.get("/")
def home():
    return {"message": "ServiceNow AI CMDB Impact Analyzer is running"}


@app.get("/check-env")
def check_env():
    return {
        "openai_key_loaded": bool(os.getenv("OPENAI_API_KEY")),
        "servicenow_url_loaded": bool(os.getenv("SERVICENOW_INSTANCE_URL")),
        "servicenow_username_loaded": bool(os.getenv("SERVICENOW_USERNAME")),
        "servicenow_password_loaded": bool(os.getenv("SERVICENOW_PASSWORD")),
    }


@app.get("/ci/{ci_name}")
def get_ci(ci_name: str):
    instance_url = os.getenv("SERVICENOW_INSTANCE_URL")
    username = os.getenv("SERVICENOW_USERNAME")
    password = os.getenv("SERVICENOW_PASSWORD")

    url = (
        f"{instance_url}/api/now/table/cmdb_ci"
        f"?sysparm_query=nameLIKE{ci_name}"
        "&sysparm_limit=1"
        "&sysparm_fields=name,sys_class_name,install_status,operational_status,sys_id"
    )

    response = requests.get(
        url,
        auth=(username, password),
        headers={"Accept": "application/json"},
        timeout=30,
    )

    data = response.json()

    if not data.get("result"):
        return {"error": f"CI {ci_name} not found"}

    return data["result"][0]


@app.get("/ai-ci/{ci_name}")
def analyze_ci(ci_name: str):
    ci = get_ci(ci_name)

    if "error" in ci:
        return ci

    return analyze_ci_with_ai(ci)


def analyze_ci_with_ai(ci: dict):
    prompt = f"""
You are a ServiceNow CMDB and CSDM impact analyst.

Analyze this Configuration Item:

Name: {ci.get("name")}
CI Class: {ci.get("sys_class_name")}
Install Status: {ci.get("install_status")}
Operational Status: {ci.get("operational_status")}

Return STRICT JSON only:

{{
  "ci_summary": "...",
  "business_impact": "...",
  "risk_level": "Low | Medium | High | Critical",
  "affected_services": ["...", "..."],
  "stakeholders_to_notify": ["...", "..."],
  "outage_blast_radius": "...",
  "change_guidance": "...",
  "recommended_actions": ["...", "...", "..."]
}}

Rules:
- Higher impact if CI appears infrastructure-related.
- If server/database/network related, assume multiple dependent services.
- Focus on ServiceNow CMDB/CSDM reasoning.
- Return JSON only.
"""

    ai_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert ServiceNow CMDB and ITOM architect. Always return valid JSON.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    ai_text = ai_response.choices[0].message.content

    try:
        parsed = json.loads(ai_text)
    except Exception:
        parsed = {
            "ci_summary": ai_text,
            "business_impact": "",
            "risk_level": "Unknown",
            "affected_services": [],
            "stakeholders_to_notify": [],
            "outage_blast_radius": "",
            "change_guidance": "",
            "recommended_actions": [],
        }

    return {
        "configuration_item": ci,
        "structured_ai": parsed,
    }
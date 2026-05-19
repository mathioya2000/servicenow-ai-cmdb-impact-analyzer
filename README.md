\# ServiceNow AI CMDB Impact Analyzer



\## Overview

AI-powered ServiceNow CMDB impact analysis assistant that evaluates Configuration Items and predicts business impact.



This project integrates:



\- ServiceNow CMDB

\- FastAPI backend

\- OpenAI API

\- Render cloud deployment

\- ServiceNow UI Action

\- GlideAjax Script Include

\- custom AI impact analysis field



\## Business Use Case

Infrastructure and platform teams need rapid impact analysis before outages or changes.



This assistant provides:



\- CI summary

\- business impact analysis

\- risk level

\- affected services

\- stakeholders to notify

\- outage blast radius

\- change guidance

\- recommended actions



\---



\## Architecture



ServiceNow Configuration Item  

↓  

UI Action: Analyze CI Impact  

↓  

GlideAjax Script Include  

↓  

FastAPI REST API on Render  

↓  

CMDB lookup  

↓  

OpenAI Analysis Engine  

↓  

Structured JSON Response  

↓  

ServiceNow AI Impact Analysis field



\---



\## API Endpoints



\### Health Check

GET /



\### CMDB Lookup

GET /ci/{ci\_name}



Example:



/ci/Oracle



\### AI Impact Analysis

GET /ai-ci/{ci\_name}



Example:



/ai-ci/Oracle



\---



\## Key Features



\- real CMDB lookup

\- CI impact analysis

\- outage blast radius

\- stakeholder recommendations

\- business impact prediction

\- CSDM-style reasoning

\- infrastructure intelligence



\---



\## Tech Stack



\- Python

\- FastAPI

\- OpenAI API

\- ServiceNow CMDB

\- GlideAjax

\- RESTMessageV2

\- Render

\- GitHub



\---



\## ServiceNow Components



\### UI Action

Configuration Item \[cmdb\_ci]



Button:



Analyze CI Impact



\### Script Include

AICMDBImpactAnalyzerAjax



\### Custom Field

u\_ai\_impact\_analysis



\### Output

Writes structured AI impact analysis into CMDB record.



\---



\## Deployment



Hosted on Render.



Environment variables:



OPENAI\_API\_KEY  

SERVICENOW\_INSTANCE\_URL  

SERVICENOW\_USERNAME  

SERVICENOW\_PASSWORD  



\---



\## Portfolio Value



Demonstrates:



\- CMDB intelligence

\- CSDM-aligned thinking

\- impact analysis

\- ServiceNow development

\- enterprise AI automation

\- infrastructure decision support



\---



\## Author



Joseph Mwangi


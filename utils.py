from typing import List, Dict
from openai import OpenAI


def generate_activation_summary(
    customer_name: str,
    industry: str,
    data_sources: List[str],
    bi_tool: str,
    refresh_cadence: str,
    priorities: List[str],
    unstructured_data: List[str],
) -> str:
    return f"""
**Customer:** {customer_name}  
**Industry:** {industry}  
**Primary data sources:** {", ".join(data_sources) if data_sources else "Not specified"}  
**BI environment:** {bi_tool}  
**Operational cadence:** {refresh_cadence}  
**Business priorities:** {", ".join(priorities) if priorities else "Not specified"}  

This activation plan is designed to deliver measurable value quickly while building an AI-ready Snowflake foundation.
The focus is on trusted data products first, then self-serve analytics, then AI-assisted decision support.
"""


def generate_architecture(
    industry: str,
    data_sources: List[str],
    refresh_cadence: str,
    bi_tool: str,
    unstructured_data: List[str],
) -> str:
    ingestion_lines = []

    if "MySQL" in data_sources:
        ingestion_lines.append("- Use CDC ingestion for MySQL operational data.")
    if "Postgres" in data_sources:
        ingestion_lines.append("- Ingest Postgres operational data into Snowflake for trusted reporting.")
    if "SQL Server" in data_sources:
        ingestion_lines.append("- Replicate SQL Server data for analytics and operational reporting.")
    if "Redshift" in data_sources:
        ingestion_lines.append("- Use Redshift as a historical backfill source while Snowflake becomes the trusted analytics environment.")
    if "BigQuery" in data_sources:
        ingestion_lines.append("- Migrate selected analytical datasets from BigQuery into governed Snowflake data products.")
    if "S3" in data_sources:
        ingestion_lines.append("- Use staged ingestion for files and event data landing in S3.")
    if "APIs" in data_sources:
        ingestion_lines.append("- Ingest API-fed operational and partner signals on a scheduled basis.")
    if "Salesforce" in data_sources:
        ingestion_lines.append("- Ingest CRM and pipeline data from Salesforce for business-facing reporting.")
    if unstructured_data:
        ingestion_lines.append("- Ingest unstructured sources as search-ready text collections with metadata.")

    ingestion_lines.append(f"- Align operational ingestion to the business cadence ({refresh_cadence}).")
    ingestion_lines.append(f"- Continue serving business reporting through {bi_tool} while Snowflake adoption grows.")

    return "\n".join(
        [
            "**Recommended architecture principles**",
            "- Keep data, AI, and governance in one platform.",
            "- Use a Bronze / Silver / Gold medallion structure.",
            "- Build AI-ready data products early (signals layer + text collections).",
            "- Separate compute using INGEST_WH, TRANSFORM_WH, BI_WH, and AI_WH.",
            "",
            "**Ingestion approach**",
            *ingestion_lines,
        ]
    )


def generate_mvps(
    industry: str,
    priorities: List[str],
    unstructured_data: List[str],
) -> List[Dict]:
    mvps = []

    if "Reduce stockouts" in priorities:
        mvps.append(
            {
                "title": "Inventory MVP",
                "scope": "Stockout risk list + recommended action, with human approval.",
                "why": "Fast operational value, clear business owner, and realistic to deliver in 90 days.",
                "outcome": "Protect revenue by catching stockout risk early and enabling faster replenishment decisions.",
            }
        )

    if "Improve customer sentiment insight" in priorities and unstructured_data:
        mvps.append(
            {
                "title": "Sentiment MVP",
                "scope": "Complaint themes + supporting citations + spike alerts.",
                "why": "Uses existing feedback data and turns disconnected text into decision-ready insight.",
                "outcome": "Detect product issues early and reduce support load.",
            }
        )

    if "Increase conversion" in priorities:
        mvps.append(
            {
                "title": "Recommendation MVP",
                "scope": "Inventory-aware bundle suggestions delivered in batch, not real-time personalization.",
                "why": "Commercially valuable but scoped tightly enough to be believable in a first activation window.",
                "outcome": "Increase conversion and average order value without long ML cycles.",
            }
        )

    if "Improve forecasting" in priorities:
        mvps.append(
            {
                "title": "Forecasting MVP",
                "scope": "Demand-risk view for planners using historical sales, promotions, and inventory context.",
                "why": "Improves planning quality without needing a full advanced ML platform on day one.",
                "outcome": "Better replenishment timing and fewer missed revenue opportunities.",
            }
        )

    if "Reduce support load" in priorities and unstructured_data:
        mvps.append(
            {
                "title": "Support Triage MVP",
                "scope": "Categorize inbound support themes and identify recurring drivers.",
                "why": "Creates immediate operational visibility from existing support content.",
                "outcome": "Reduce manual triage effort and speed up issue identification.",
            }
        )

    if "Improve promotion effectiveness" in priorities:
        mvps.append(
            {
                "title": "Promotion Effectiveness MVP",
                "scope": "Measure promotion lift, margin impact, and inventory effect across campaigns.",
                "why": "Directly ties data activation to commercial decision-making.",
                "outcome": "Improve campaign quality and reduce wasted promotional spend.",
            }
        )

    return mvps


def generate_roadmap(
    priorities: List[str],
    refresh_cadence: str,
    unstructured_data: List[str],
) -> List[Dict]:
    roadmap = [
        {
            "phase": "Days 1–30: Platform Foundation and Initial Value",
            "objectives": [
                "Establish Snowflake as a trusted analytics environment for priority workloads.",
                "Ingest core structured data quickly.",
                "Deliver early visibility into inventory and demand trends.",
            ],
            "deliverables": [
                "Landing zone setup with environments, RBAC, and warehouse structure.",
                "Initial ingestion of core operational data sources.",
                "Historical backfill from legacy warehouse where needed.",
                f"Operational ingestion aligned to {refresh_cadence}.",
                "Validated business-ready datasets for first reporting use cases.",
                "Initial dashboards for priority business teams.",
            ],
            "teams": [
                "Data engineering team",
                "Analytics team",
                "Business stakeholders",
            ],
        },
        {
            "phase": "Days 30–60: Self-Serve Analytics and Customer Insight",
            "objectives": [
                "Enable business users to explore data without waiting on analysts.",
                "Turn customer feedback into usable insight.",
                "Build trust in Snowflake as both a reporting and insight platform.",
            ],
            "deliverables": [
                "Governed self-serve analytics capability.",
                "Search-ready text insight layer." if unstructured_data else "Prepare text insight capability if unstructured data becomes available.",
                "Customer or operational trend reporting.",
                "Business examples showing how natural language questions map to decisions.",
            ],
            "teams": [
                "Analytics team",
                "Business stakeholders",
                "Customer support / CX team" if unstructured_data else "Operations team",
            ],
        },
        {
            "phase": "Days 60–90: AI-Assisted Decision Support",
            "objectives": [
                "Introduce scoped AI workflows that support operational decisions.",
                "Keep humans in the approval loop.",
                "Demonstrate movement from reporting into AI-assisted action.",
            ],
            "deliverables": [
                "At least one operational decision-support workflow.",
                "Alerting or recommendation workflow tied to business priorities.",
                "Approval and monitoring framework for AI recommendations.",
            ],
            "teams": [
                "Business owners",
                "Analytics team",
                "Operational teams",
            ],
        },
    ]

    return roadmap


def generate_handover(fiscal_timing: str) -> str:
    if fiscal_timing == "Near end of quarter/year":
        return """
**Recommended handover:** Acquisition Solution Engineer

At the end of the 90-day activation, the customer should have:
- a stable landing zone
- validated business data products
- at least one functioning AI-assisted workflow
- clear ownership of pipelines, analytics assets, and usage monitoring

Because this handover occurs near the end of the fiscal period, responsibility would return to the **Acquisition Solution Engineer** for continued onboarding and early consumption growth.
"""
    return """
**Recommended handover:** Expansion Solution Engineer

At the end of the 90-day activation, the customer should have:
- a stable landing zone
- validated business data products
- at least one functioning AI-assisted workflow
- clear ownership of pipelines, analytics assets, and usage monitoring

Because there is still good time left in the fiscal year, responsibility would transition to the **Expansion Solution Engineer** to scale adoption across departments and introduce additional AI workloads.
"""


def generate_agent_templates(
    industry: str,
    priorities: List[str],
) -> List[Dict]:
    agents = []

    if "Reduce stockouts" in priorities:
        agents.append(
            {
                "name": "Inventory Risk Agent",
                "purpose": "Identify SKUs at risk of stockout and recommend actions.",
                "inputs": ["inventory snapshots", "sales velocity", "product metadata"],
                "pattern": "Sense → Reason → Propose → Approve → Track",
            }
        )

    if "Improve customer sentiment insight" in priorities:
        agents.append(
            {
                "name": "Sentiment Spike Agent",
                "purpose": "Detect emerging complaint spikes in customer feedback.",
                "inputs": ["reviews", "support tickets", "return reasons", "product metadata"],
                "pattern": "Sense → Reason → Propose → Approve → Track",
            }
        )

    if "Increase conversion" in priorities:
        agents.append(
            {
                "name": "Bundle Recommendation Agent",
                "purpose": "Suggest inventory-aware bundles for campaigns.",
                "inputs": ["order history", "product affinity data", "inventory availability"],
                "pattern": "Sense → Reason → Propose → Approve → Track",
            }
        )

    if "Improve forecasting" in priorities:
        agents.append(
            {
                "name": "Demand Forecast Agent",
                "purpose": "Highlight likely demand spikes and planning risks.",
                "inputs": ["sales history", "promotion calendar", "inventory position"],
                "pattern": "Sense → Reason → Propose → Approve → Track",
            }
        )

    if "Reduce support load" in priorities:
        agents.append(
            {
                "name": "Support Triage Agent",
                "purpose": "Classify inbound issues and surface recurring themes.",
                "inputs": ["tickets", "chat transcripts", "case metadata"],
                "pattern": "Sense → Reason → Propose → Approve → Track",
            }
        )

    if "Improve promotion effectiveness" in priorities:
        agents.append(
            {
                "name": "Promotion Advisor Agent",
                "purpose": "Assess campaign performance and suggest where to optimize.",
                "inputs": ["campaign data", "sales performance", "margin data", "inventory context"],
                "pattern": "Sense → Reason → Propose → Approve → Track",
            }
        )

    return agents


def enhance_plan_with_llm(
    api_key: str,
    customer_name: str,
    industry: str,
    data_sources: list,
    bi_tool: str,
    refresh_cadence: str,
    priorities: list,
    unstructured_data: list,
    fiscal_timing: str,
    summary: str,
    architecture: str,
    mvps: list,
    roadmap: list,
    handover: str,
    agents: list,
) -> str:
    client = OpenAI(api_key=api_key)

    prompt = f"""
You are a Snowflake Activation Engineer preparing an executive-ready activation plan.

Rewrite the following deterministic activation blueprint into polished, commercially credible markdown.

Customer name: {customer_name}
Industry: {industry}
Data sources: {", ".join(data_sources) if data_sources else "Not specified"}
BI tool: {bi_tool}
Refresh cadence: {refresh_cadence}
Business priorities: {", ".join(priorities) if priorities else "Not specified"}
Unstructured data: {", ".join(unstructured_data) if unstructured_data else "None"}
Fiscal timing: {fiscal_timing}

RULE-BASED SUMMARY:
{summary}

RULE-BASED ARCHITECTURE:
{architecture}

RULE-BASED MVPS:
{mvps}

RULE-BASED ROADMAP:
{roadmap}

RULE-BASED HANDOVER:
{handover}

RULE-BASED AGENTS:
{agents}

Return markdown with these sections:
1. Executive Summary
2. Recommended Architecture
3. Thin-Slice MVPs
4. 30-60-90 Activation Plan
5. Handover Recommendation
6. Suggested Agent Templates

Keep it realistic, concise, polished, and easy to present in an interview.
"""

    response = client.responses.create(
        model="gpt-5",
        input=prompt,
    )

    return response.output_text
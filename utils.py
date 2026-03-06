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
    industry_context = {
        "Retail": "The activation should focus on inventory visibility, demand signals, promotion impact, and customer feedback loops.",
        "Financial Services": "The activation should focus on governed analytics, risk visibility, operational reporting, and carefully controlled AI use cases.",
        "Manufacturing": "The activation should focus on supply chain visibility, production signals, operational efficiency, and planning quality.",
        "Healthcare": "The activation should focus on trusted governed data, reporting consistency, operational insight, and tightly scoped AI assistance.",
        "Other": "The activation should focus on trusted data foundations, measurable business outcomes, and scoped AI-assisted workflows.",
    }

    cadence_implication = {
        "Real-time": "This customer likely needs low-latency data movement for operational decisions.",
        "15 minutes": "This customer likely needs near-real-time operational visibility without full streaming complexity.",
        "Hourly": "This customer can support operational reporting with frequent refreshes and governed datasets.",
        "Daily": "This customer is likely best suited to batch-oriented activation use cases first.",
    }

    return f"""
**Customer:** {customer_name}  
**Industry:** {industry}  
**Primary data sources:** {", ".join(data_sources) if data_sources else "Not specified"}  
**BI environment:** {bi_tool}  
**Operational cadence:** {refresh_cadence}  
**Business priorities:** {", ".join(priorities) if priorities else "Not specified"}  
**Unstructured data available:** {", ".join(unstructured_data) if unstructured_data else "None"}  

{industry_context.get(industry, industry_context["Other"])}
{cadence_implication.get(refresh_cadence, "")}

This activation plan is designed to deliver measurable value quickly while building an AI-ready Snowflake foundation.  
The first goal is to create trusted data products for priority business decisions, then enable self-serve insight, then introduce scoped AI-assisted workflows.
"""


def generate_architecture(
    industry: str,
    data_sources: List[str],
    refresh_cadence: str,
    bi_tool: str,
    unstructured_data: List[str],
) -> str:
    industry_lines = {
        "Retail": "- Prioritize inventory, sales, promotion, and customer-feedback data products.",
        "Financial Services": "- Prioritize governed access controls, auditability, and risk-sensitive data domains.",
        "Manufacturing": "- Prioritize supply chain, plant operations, inventory, and demand-planning data products.",
        "Healthcare": "- Prioritize governance, sensitive-data controls, and trusted operational reporting layers.",
        "Other": "- Prioritize the business domains most closely tied to measurable near-term value.",
    }

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
    else:
        ingestion_lines.append("- Start with structured data products first, then add text pipelines later if needed.")

    cadence_lines = {
        "Real-time": "- Use low-latency ingestion patterns only for the highest-value operational signals.",
        "15 minutes": "- Use frequent micro-batch ingestion to balance freshness and operational simplicity.",
        "Hourly": "- Use hourly operational refreshes for decision support and reporting alignment.",
        "Daily": "- Use scheduled batch pipelines with emphasis on reliability, data quality, and governance.",
    }

    return "\n".join(
        [
            "**Recommended architecture principles**",
            "- Keep data, AI, and governance in one platform.",
            "- Use a Bronze / Silver / Gold medallion structure.",
            "- Build AI-ready data products early, including business signals and text collections where available.",
            "- Separate compute using INGEST_WH, TRANSFORM_WH, BI_WH, and AI_WH.",
            industry_lines.get(industry, industry_lines["Other"]),
            "",
            "**Ingestion approach**",
            *ingestion_lines,
            cadence_lines.get(refresh_cadence, ""),
            f"- Continue serving business reporting through {bi_tool} while Snowflake adoption grows.",
        ]
    )


def generate_mvps(
    industry: str,
    priorities: List[str],
    unstructured_data: List[str],
) -> List[Dict]:
    mvps = []

    if "Reduce stockouts" in priorities:
        scope = "Stockout risk list + recommended action, with human approval."
        if industry == "Manufacturing":
            scope = "Material or SKU shortage risk list + recommended planning action, with human approval."
        mvps.append(
            {
                "title": "Inventory MVP",
                "scope": scope,
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
    industry: str,
    priorities: List[str],
    refresh_cadence: str,
    unstructured_data: List[str],
) -> List[Dict]:
    days_1_30_objectives = [
        "Establish Snowflake as a trusted analytics environment for priority workloads.",
        "Ingest core structured data quickly.",
        "Stand up the first business-ready datasets tied to near-term value.",
    ]
    days_1_30_deliverables = [
        "Landing zone setup with environments, RBAC, and warehouse structure.",
        "Initial ingestion of core operational data sources.",
        f"Operational ingestion aligned to {refresh_cadence}.",
        "Validated business-ready datasets for first reporting use cases.",
    ]
    days_1_30_teams = ["Data engineering team", "Analytics team", "Business stakeholders"]

    if "Reduce stockouts" in priorities:
        days_1_30_objectives.append("Deliver early visibility into inventory risk and sales velocity.")
        days_1_30_deliverables.extend(
            [
                "Inventory position and sales-velocity datasets.",
                "Initial stockout-risk reporting for merchandising or supply chain teams.",
            ]
        )

    if "Improve promotion effectiveness" in priorities:
        days_1_30_deliverables.append("Promotion performance dataset with initial business reporting.")

    days_30_60_objectives = [
        "Enable business users to explore data without waiting on analysts.",
        "Build trust in Snowflake as both a reporting and insight platform.",
    ]
    days_30_60_deliverables = [
        "Governed self-serve analytics capability.",
        "Business examples showing how natural language questions map to decisions.",
    ]
    days_30_60_teams = ["Analytics team", "Business stakeholders"]

    if "Improve customer sentiment insight" in priorities and unstructured_data:
        days_30_60_objectives.append("Turn customer feedback into usable insight.")
        days_30_60_deliverables.extend(
            [
                "Search-ready text insight layer across reviews, tickets, or return reasons.",
                "Complaint theme reporting with citations and trend visibility.",
            ]
        )
        days_30_60_teams.append("Customer support / CX team")

    if "Reduce support load" in priorities and unstructured_data:
        days_30_60_deliverables.append("Support theme analysis and triage visibility.")

    if industry == "Financial Services":
        days_30_60_deliverables.append("Governed access patterns and business-facing auditability examples.")

    days_60_90_objectives = [
        "Introduce scoped AI workflows that support operational decisions.",
        "Keep humans in the approval loop.",
        "Demonstrate movement from reporting into AI-assisted action.",
    ]
    days_60_90_deliverables = [
        "Approval and monitoring framework for AI recommendations.",
    ]
    days_60_90_teams = ["Business owners", "Analytics team", "Operational teams"]

    if "Reduce stockouts" in priorities:
        days_60_90_deliverables.append("Inventory risk workflow generating prioritized replenishment recommendations.")
    if "Increase conversion" in priorities:
        days_60_90_deliverables.append("Batch recommendation MVP for merchandising or campaign planning.")
    if "Improve forecasting" in priorities:
        days_60_90_deliverables.append("Forecast-oriented decision support workflow for planners.")
    if "Improve customer sentiment insight" in priorities and unstructured_data:
        days_60_90_deliverables.append("Sentiment spike alert workflow for customer or product teams.")
    if "Reduce support load" in priorities and unstructured_data:
        days_60_90_deliverables.append("Support triage assistant for recurring issue detection.")
    if "Improve promotion effectiveness" in priorities:
        days_60_90_deliverables.append("Promotion advisor workflow for campaign review and optimization.")

    if len(days_60_90_deliverables) == 1:
        days_60_90_deliverables.insert(0, "At least one operational decision-support workflow tied to a priority use case.")

    return [
        {
            "phase": "Days 1–30: Platform Foundation and Initial Value",
            "objectives": days_1_30_objectives,
            "deliverables": days_1_30_deliverables,
            "teams": days_1_30_teams,
        },
        {
            "phase": "Days 30–60: Self-Serve Analytics and Customer Insight",
            "objectives": days_30_60_objectives,
            "deliverables": days_30_60_deliverables,
            "teams": days_30_60_teams,
        },
        {
            "phase": "Days 60–90: AI-Assisted Decision Support",
            "objectives": days_60_90_objectives,
            "deliverables": days_60_90_deliverables,
            "teams": days_60_90_teams,
        },
    ]


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
        agent_name = "Inventory Risk Agent"
        purpose = "Identify SKUs at risk of stockout and recommend actions."
        if industry == "Manufacturing":
            agent_name = "Supply Risk Agent"
            purpose = "Identify parts or materials at risk of shortage and recommend actions."
        agents.append(
            {
                "name": agent_name,
                "purpose": purpose,
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
You are a Snowflake Activation Engineer preparing a sharp executive-ready activation recommendation.

Use the structured inputs below to produce a more thoughtful, customer-specific plan.

Customer name: {customer_name}
Industry: {industry}
Data sources: {", ".join(data_sources) if data_sources else "Not specified"}
BI tool: {bi_tool}
Refresh cadence: {refresh_cadence}
Business priorities: {", ".join(priorities) if priorities else "Not specified"}
Unstructured data: {", ".join(unstructured_data) if unstructured_data else "None"}
Fiscal timing: {fiscal_timing}

Base summary:
{summary}

Base architecture:
{architecture}

Base MVPs:
{mvps}

Base roadmap:
{roadmap}

Base handover:
{handover}

Base agents:
{agents}

Return markdown with these sections:

# Executive Summary
A concise commercial summary of the customer situation and activation objective.

# Recommended First MVP
Choose the single best MVP to lead with and explain why.

# Recommended Snowflake Architecture
Make this specific to the customer context.

# 30-60-90 Plan
Make each phase specific to the selected priorities.

# Risks and Dependencies
List the main delivery risks or assumptions.

# Success Metrics
Give 4-6 measurable outcomes.

# Executive Talk Track
Write a short spoken talk track I could use in a customer meeting.

Be specific, commercially realistic, and avoid generic filler.
"""

    response = client.responses.create(
        model="gpt-5",
        input=prompt,
    )

    return response.output_text
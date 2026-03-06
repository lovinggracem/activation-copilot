from typing import Dict, List


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
**Unstructured data available:** {", ".join(unstructured_data) if unstructured_data else "None specified"}  

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
        ingestion_lines.append("- Use CDC or scheduled replication for Postgres transactional data.")
    if "SQL Server" in data_sources:
        ingestion_lines.append("- Use structured batch or CDC pipelines for SQL Server workloads.")
    if "Redshift" in data_sources:
        ingestion_lines.append(
            "- Use Redshift as a historical backfill source while Snowflake becomes the trusted analytics environment."
        )
    if "BigQuery" in data_sources:
        ingestion_lines.append("- Backfill curated analytics datasets from BigQuery where needed.")
    if "S3" in data_sources:
        ingestion_lines.append("- Land files from S3 into a governed ingestion zone for batch processing.")
    if "APIs" in data_sources:
        ingestion_lines.append("- Use API ingestion for operational signals that are not available in core databases.")
    if "Salesforce" in data_sources:
        ingestion_lines.append("- Replicate CRM data to join pipeline, customer, and commercial signals.")
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
            f"- Tailor the semantic layer and KPIs to {industry.lower()} decision workflows.",
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
                "scope": "SKU or category-level demand forecast with exception reporting for planners.",
                "why": "Creates a decision-ready planning asset without requiring a large ML platform build first.",
                "outcome": "Improve ordering decisions and reduce overstock or missed demand.",
            }
        )

    if "Improve promotion effectiveness" in priorities:
        mvps.append(
            {
                "title": "Promotion Performance MVP",
                "scope": "Post-promotion analysis showing lift, margin impact, and inventory effects.",
                "why": "Helps commercial teams decide which promotion patterns to repeat or retire.",
                "outcome": "Improve promotional ROI and reduce avoidable discounting.",
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
                "Deliver early visibility into operational performance and demand trends.",
            ],
            "deliverables": [
                "Landing zone setup with environments, RBAC, and warehouse structure.",
                "Core structured ingestion for priority systems.",
                "Historical backfill from legacy warehouse if needed.",
                f"Operational ingestion aligned to {refresh_cadence}.",
                "Validated KPI datasets for early executive and operator reporting.",
                "Initial dashboards for business and analytics stakeholders.",
            ],
            "teams": [
                "Data engineering team",
                "Analytics team",
                "Business domain stakeholders",
                "Platform owners",
            ],
        },
        {
            "phase": "Days 30–60: Self-Serve Analytics and Customer Insight",
            "objectives": [
                "Enable business users to explore data without waiting on analysts.",
                "Turn customer or operational feedback into usable insight.",
                "Build trust in Snowflake as both a reporting and insight platform.",
            ],
            "deliverables": [
                "Governed self-serve analytics patterns for business users.",
                "Cortex Search or equivalent text exploration capability over unstructured sources."
                if unstructured_data
                else "Text insight capability if unstructured data becomes available.",
                "Insight dashboards and trend reporting tied to business priorities.",
                "Business examples showing how natural-language questions map to decisions.",
            ],
            "teams": [
                "Analytics team",
                "Business users",
                "Customer support / CX team" if unstructured_data else "Operations team",
                "Product or commercial stakeholders",
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
                "At least one thin-slice AI workflow tied to a priority business use case.",
                "Monitoring, approval, and exception-handling framework.",
                "Operational playbook for ownership and adoption.",
                "Business readout demonstrating value, usage, and next-step expansion.",
            ],
            "teams": [
                "Business process owners",
                "Analytics and data team",
                "Operations or commercial team",
                "Executive sponsors",
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
                "purpose": "Surface forecast exceptions and planning risks for the next ordering cycle.",
                "inputs": ["historical sales", "promotions", "inventory levels", "seasonality signals"],
                "pattern": "Sense → Forecast → Flag → Review → Act",
            }
        )

    if "Improve promotion effectiveness" in priorities:
        agents.append(
            {
                "name": "Promotion Review Agent",
                "purpose": "Summarize promotion lift, margin impact, and repeatability.",
                "inputs": ["campaign data", "sales results", "margin data", "inventory impact"],
                "pattern": "Sense → Compare → Explain → Recommend → Track",
            }
        )

    return agents

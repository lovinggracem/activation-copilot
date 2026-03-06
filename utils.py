from __future__ import annotations

import json
import re
from io import BytesIO
from typing import Any

from openai import OpenAI
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer


def _fmt_list(items: list[str]) -> str:
    return ", ".join(items) if items else "None provided"


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def generate_activation_summary(
    customer_name: str,
    industry: str,
    data_sources: list[str],
    bi_tool: str,
    refresh_cadence: str,
    priorities: list[str],
    unstructured_data: list[str],
) -> str:
    priorities_text = _fmt_list(priorities)
    sources_text = _fmt_list(data_sources)
    unstructured_text = _fmt_list(unstructured_data)

    industry_angle = {
        "Retail": (
            "The customer appears to be at a common retail inflection point: they have enough operational and "
            "customer data to create value quickly, but not yet a unified way to turn that data into consistent "
            "decisions across merchandising, inventory, support, and digital channels."
        ),
        "Financial Services": (
            "The customer appears to be balancing growth, control, and time-to-insight. The likely challenge is "
            "not data scarcity, but fragmented access to trusted data across analytical, operational, and customer-facing use cases."
        ),
        "Manufacturing": (
            "The customer appears to be in a position where operational data exists across multiple systems, but "
            "the business needs a clearer path from raw data to production, supply chain, and service decisions."
        ),
        "Healthcare": (
            "The customer appears to be managing multiple data sources with a strong need for trust, governance, "
            "and practical adoption, especially where operational decisions depend on timely and consistent insight."
        ),
        "Other": (
            "The customer appears to have meaningful data assets already in place, but needs a practical activation "
            "path that connects data consolidation to measurable business outcomes."
        ),
    }.get(industry, "")

    priority_outcome = {
        "Reduce stockouts": "improve product availability and reduce missed revenue from out-of-stock items",
        "Improve customer sentiment insight": "surface customer pain points earlier and improve response quality",
        "Increase conversion": "improve the quality and timing of customer-facing decisions that influence purchase behavior",
        "Improve forecasting": "produce more confident demand and planning signals",
        "Reduce support load": "help teams identify drivers of contact volume and reduce avoidable support effort",
        "Improve promotion effectiveness": "improve promotional targeting, timing, and post-campaign understanding",
    }

    mapped_outcomes = [priority_outcome[p] for p in priorities if p in priority_outcome]
    if mapped_outcomes:
        if len(mapped_outcomes) == 1:
            outcome_sentence = f"Near-term success should focus on using Snowflake to {mapped_outcomes[0]}."
        elif len(mapped_outcomes) == 2:
            outcome_sentence = (
                f"Near-term success should focus on using Snowflake to {mapped_outcomes[0]} "
                f"and {mapped_outcomes[1]}."
            )
        else:
            outcome_sentence = (
                "Near-term success should focus on using Snowflake to "
                + ", ".join(mapped_outcomes[:-1])
                + f", and {mapped_outcomes[-1]}."
            )
    else:
        outcome_sentence = "Near-term success should focus on using Snowflake to create measurable business value quickly."

    return f"""**Customer:** {customer_name}

**Industry:** {industry}

**Current landscape:** The customer is working with data from {sources_text} and currently relies on {bi_tool} for business reporting. The target operating cadence suggests the business wants data products that can support **{refresh_cadence.lower()}** decision-making rather than purely retrospective reporting.

**Business priorities:** {priorities_text}

**Available unstructured signals:** {unstructured_text}

{industry_angle}

From an activation perspective, the most practical first step is not trying to transform every part of the data estate at once. Instead, the customer should establish a trusted core data foundation in Snowflake, connect that foundation to a small number of high-visibility use cases, and prove value with thin-slice deliverables that the business can understand quickly.

{outcome_sentence}

A strong activation plan for this customer should therefore do three things in parallel: create trusted access to core data, deliver one or more business-visible MVPs, and build enough internal confidence that the customer can continue expanding after the initial 90-day engagement."""


def generate_architecture(
    industry: str,
    data_sources: list[str],
    refresh_cadence: str,
    bi_tool: str,
    unstructured_data: list[str],
) -> str:
    source_ingestion = [
        f"Ingest structured data from **{source}** into Snowflake through a repeatable landing and transformation pattern."
        for source in data_sources
    ] or ["Ingest priority business data into Snowflake through a repeatable landing and transformation pattern."]

    unstructured_layer = []
    if unstructured_data:
        unstructured_layer.append(
            f"Bring unstructured sources into the platform as governed analytical assets, including **{_fmt_list(unstructured_data)}**."
        )
        unstructured_layer.append(
            "Use document and text processing patterns so unstructured data can support sentiment, theme extraction, root-cause analysis, and agent experiences."
        )

    cadence_guidance = {
        "Real-time": "Design pipelines for near-real-time ingestion only where the use case truly needs it; avoid unnecessary complexity for lower-value domains.",
        "15 minutes": "Use a frequent micro-batch pattern so the business can react quickly without overengineering for full streaming everywhere.",
        "Hourly": "Use hourly refresh patterns for core data products, with tighter SLAs only for clearly justified operational workflows.",
        "Daily": "Use daily refresh for foundational reporting and introduce faster refresh selectively for the most time-sensitive decisions.",
    }.get(refresh_cadence, "Choose refresh patterns based on business urgency and operational value.")

    industry_principles = {
        "Retail": [
            "Model around products, inventory positions, sales, channels, customers, and service events.",
            "Prioritize inventory and demand visibility so commercial teams can act on emerging changes quickly.",
        ],
        "Financial Services": [
            "Prioritize governed access, auditable transformations, and clear domain ownership.",
            "Separate exploratory data use from controlled production-grade data products.",
        ],
        "Manufacturing": [
            "Model around plants, production events, inventory, suppliers, logistics, and service signals.",
            "Design for operational visibility and bottleneck identification across the supply chain.",
        ],
        "Healthcare": [
            "Prioritize governance, lineage, and controlled access to sensitive or regulated data domains.",
            "Focus early on high-trust curated data products for operational and analytical teams.",
        ],
        "Other": [
            "Model key business entities in a way that supports both analytics and future AI use cases.",
            "Keep the first architecture simple, governed, and expandable.",
        ],
    }.get(industry, [])

    sections = [
        "**Recommended architecture principles**",
        "- Establish Snowflake as the governed data foundation for both analytics and future AI workloads.",
        "- Create a clear path from raw ingestion to curated business-ready data products.",
        f"- Keep {bi_tool} connected to Snowflake for continuity, while improving trust and freshness of the underlying data.",
        f"- {cadence_guidance}",
        "",
        "**Suggested architecture flow**",
        "- Source systems -> ingestion layer -> raw landing zone -> transformed domain models -> curated business marts -> BI, operational use cases, and AI applications.",
        "- Introduce lightweight orchestration and data quality checks early so the first MVPs are trusted.",
        "- Build semantic consistency across core entities before expanding to broader use cases.",
        "",
        "**Ingestion focus**",
        _bullets(source_ingestion),
    ]

    if unstructured_layer:
        sections.extend(["", "**Unstructured and AI-ready layer**", _bullets(unstructured_layer)])

    if industry_principles:
        sections.extend(["", "**Industry-specific emphasis**", _bullets(industry_principles)])

    sections.extend(
        [
            "",
            "**Why this architecture first**",
            "- It creates an immediate path to business value without requiring a full enterprise redesign.",
            "- It keeps the customer’s existing BI motion intact while improving data trust.",
            "- It sets up the customer for both near-term reporting wins and later AI expansion.",
        ]
    )

    return "\n".join(sections)


def generate_mvps(
    industry: str,
    priorities: list[str],
    unstructured_data: list[str],
) -> list[dict[str, str]]:
    mvps: list[dict[str, str]] = []

    has_reviews = "Product reviews" in unstructured_data
    has_support = "Support tickets" in unstructured_data
    has_returns = "Return reasons" in unstructured_data
    has_chat = "Chat transcripts" in unstructured_data
    has_emails = "Emails" in unstructured_data

    if "Reduce stockouts" in priorities:
        mvps.append(
            {
                "title": "Inventory MVP: Stockout Risk View",
                "scope": (
                    "Create a daily or intra-day inventory risk view that highlights fast-selling products, low cover positions, "
                    "location or channel exposure, and a prioritized reorder or intervention list."
                ),
                "why": (
                    "This is commercially visible, easy for the business to understand, and directly tied to revenue protection."
                ),
                "outcome": (
                    "Merchandising and operations teams can identify likely stockouts earlier and take action before availability issues become customer-impacting."
                ),
            }
        )

    if "Improve customer sentiment insight" in priorities:
        evidence = []
        if has_reviews:
            evidence.append("product reviews")
        if has_support:
            evidence.append("support tickets")
        if has_returns:
            evidence.append("return reasons")
        if has_chat:
            evidence.append("chat transcripts")
        if has_emails:
            evidence.append("emails")

        mvps.append(
            {
                "title": "Sentiment MVP: Customer Pain-Point Intelligence",
                "scope": (
                    "Aggregate customer feedback signals and categorize the main complaint, praise, and friction themes, "
                    "with a simple view of spike areas by product, journey stage, or issue type."
                ),
                "why": (
                    "This turns unstructured data into immediate operational insight and helps prove that Snowflake can support more than standard BI use cases."
                ),
                "outcome": (
                    f"Support, product, and commercial teams can quickly see where customer experience is deteriorating using signals from {_fmt_list(evidence) if evidence else 'available customer feedback sources'}."
                ),
            }
        )

    if "Increase conversion" in priorities:
        mvps.append(
            {
                "title": "Conversion MVP: Opportunity and Friction Signals",
                "scope": (
                    "Create a focused conversion view that combines sales or funnel performance with customer behavior or sentiment indicators "
                    "to highlight where the customer journey is underperforming."
                ),
                "why": (
                    "This links data activation directly to growth outcomes and creates an executive-friendly narrative around measurable commercial impact."
                ),
                "outcome": (
                    "Commercial teams can identify specific journey friction points and prioritize the highest-impact opportunities to improve conversion."
                ),
            }
        )

    if "Improve forecasting" in priorities:
        mvps.append(
            {
                "title": "Forecasting MVP: Demand Signal Starter",
                "scope": (
                    "Create an initial planning dataset that combines recent sales, seasonality indicators, inventory position, "
                    "and key customer signals to support a more reliable short-horizon demand view."
                ),
                "why": (
                    "Forecasting is a natural extension of trusted data consolidation and creates a bridge to more advanced planning use cases."
                ),
                "outcome": (
                    "Planning teams gain a more consistent baseline view of demand risk and can reduce reactive decision-making."
                ),
            }
        )

    if "Reduce support load" in priorities:
        mvps.append(
            {
                "title": "Support MVP: Contact Driver Analysis",
                "scope": (
                    "Classify and trend the major drivers of incoming support demand, with visibility into repeat issues, avoidable contacts, and escalation hotspots."
                ),
                "why": (
                    "This is often quick to show value and demonstrates how structured plus unstructured data can improve operational efficiency."
                ),
                "outcome": (
                    "Service leaders can see the main causes of contact volume and target the highest-value reduction opportunities."
                ),
            }
        )

    if "Improve promotion effectiveness" in priorities:
        mvps.append(
            {
                "title": "Promotion MVP: Campaign Performance and Response View",
                "scope": (
                    "Create a focused view of promotion performance by product, audience, timing, and outcome so the business can compare what worked and what did not."
                ),
                "why": (
                    "This creates a clear commercial narrative and can often be delivered quickly from existing sales and campaign data."
                ),
                "outcome": (
                    "Marketing and commercial teams can make more informed decisions about which promotions to scale, adjust, or stop."
                ),
            }
        )

    return mvps[:3]


def generate_roadmap(
    industry: str,
    priorities: list[str],
    refresh_cadence: str,
    unstructured_data: list[str],
) -> list[dict[str, Any]]:
    days_1_30 = {
        "phase": "Days 1-30: Foundation and First Value",
        "objectives": [
            "Confirm business success criteria, priority stakeholders, and decision-makers.",
            "Land the first priority data domains in Snowflake and validate data access patterns.",
            "Define the first thin-slice MVPs and align on what 'good' looks like.",
            "Establish the basic governance, transformation, and quality controls needed for trust.",
        ],
        "deliverables": [
            "Discovery readout and activation scope.",
            "Initial source-to-Snowflake ingestion pattern.",
            "Draft curated data model for first business use cases.",
            "Agreed MVP definitions, owners, and success measures.",
        ],
        "teams": [
            "Data and analytics engineering",
            "Business stakeholders for the selected use cases",
            "Platform and architecture owners",
        ],
    }

    days_31_60 = {
        "phase": "Days 31-60: MVP Build and Operational Readiness",
        "objectives": [
            "Build and validate the first MVP data products.",
            "Connect curated outputs to business workflows, reporting, or AI use cases.",
            f"Operationalize data refresh patterns aligned to the target cadence of {refresh_cadence.lower()}.",
            "Document assumptions, known risks, and next scaling decisions.",
        ],
        "deliverables": [
            "Working MVP outputs for priority business use cases.",
            "Validation sessions with business users and feedback loops.",
            "Data quality checks and monitoring for critical flows.",
            "Adoption guidance for the initial user groups.",
        ],
        "teams": [
            "Analytics and BI users",
            "Operational stakeholders tied to the MVPs",
            "Data engineering and platform teams",
        ],
    }

    days_61_90 = {
        "phase": "Days 61-90: Scale, Adoption, and Handover",
        "objectives": [
            "Refine MVPs based on user feedback and usage patterns.",
            "Create a clear expansion path from initial use cases to the next wave of activation.",
            "Transfer ownership patterns, documentation, and operating guidance to the customer team.",
            "Leave the customer with a practical roadmap for post-engagement execution.",
        ],
        "deliverables": [
            "Refined MVPs with feedback incorporated.",
            "Phase-two activation recommendations.",
            "Handover pack covering architecture, ownership, and next steps.",
            "Customer enablement sessions and operational run guidance.",
        ],
        "teams": [
            "Customer data team",
            "Business sponsors",
            "Account team and customer success counterparts",
        ],
    }

    if industry == "Retail":
        days_1_30["deliverables"].append(
            "Baseline inventory, demand, and customer-signal views for rapid commercial prioritization."
        )
        days_31_60["deliverables"].append(
            "Operational stockout, sentiment, or conversion MVPs ready for stakeholder review."
        )

    if unstructured_data:
        days_31_60["objectives"].append(
            "Introduce text or feedback signal processing where it supports the selected MVPs."
        )

    if priorities:
        days_61_90["objectives"].append(
            "Define the next two to three use cases that logically follow from the initial priority set."
        )

    return [days_1_30, days_31_60, days_61_90]


def generate_handover(fiscal_timing: str) -> str:
    commercial_note = {
        "Near end of quarter/year": (
            "Because the customer is close to a fiscal boundary, the handover should emphasize clear ownership, "
            "quick-win evidence, and a realistic prioritization of what must happen next versus what can wait."
        ),
        "Good time left in fiscal year": (
            "Because the customer has room left in the fiscal cycle, the handover can balance short-term wins "
            "with a cleaner path to the next wave of platform and use-case expansion."
        ),
    }.get(
        fiscal_timing,
        "The handover should balance short-term proof with a practical path to continued execution."
    )

    return f"""By Day 90, the customer should not just have a set of deliverables — they should have a clearer operating model for how to continue.

**Recommended handover elements**
- Confirm ownership across data engineering, analytics, business stakeholders, and executive sponsors.
- Document the production flow from source ingestion through curated outputs and consumption layers.
- Capture known risks, dependencies, and deferred design decisions.
- Provide a sequenced next-step roadmap covering both platform work and business use cases.
- Ensure the account team understands where the customer has momentum and where additional support may be needed.

{commercial_note}

A strong Day 90 handover should leave the customer able to say: we understand what has been built, why it matters, who owns it, and what the next logical expansion steps are."""


def generate_agent_templates(
    industry: str,
    priorities: list[str],
) -> list[dict[str, Any]]:
    agents: list[dict[str, Any]] = []

    if "Reduce stockouts" in priorities:
        agents.append(
            {
                "name": "Stockout Risk Agent",
                "purpose": "Summarize products or locations at highest risk of stockout and explain the likely driver.",
                "inputs": [
                    "Inventory position",
                    "Recent sales velocity",
                    "Replenishment lead time",
                    "Channel or location context",
                ],
                "pattern": "Monitor -> rank risk -> explain likely cause -> recommend action",
            }
        )

    if "Improve customer sentiment insight" in priorities:
        agents.append(
            {
                "name": "Customer Signal Agent",
                "purpose": "Summarize emerging complaint themes, sentiment shifts, and likely operational root causes.",
                "inputs": [
                    "Support tickets",
                    "Reviews or feedback text",
                    "Return reasons",
                    "Product or customer segment metadata",
                ],
                "pattern": "Ingest text -> classify themes -> detect spikes -> summarize implications",
            }
        )

    if "Increase conversion" in priorities:
        agents.append(
            {
                "name": "Conversion Insight Agent",
                "purpose": "Highlight likely friction points in the purchase journey and prioritize actions to improve conversion.",
                "inputs": [
                    "Sales or funnel data",
                    "Customer behavior signals",
                    "Campaign or channel context",
                    "Customer feedback indicators",
                ],
                "pattern": "Compare journey stages -> identify drop-offs -> connect to likely drivers -> suggest interventions",
            }
        )

    if "Improve forecasting" in priorities:
        agents.append(
            {
                "name": "Demand Planning Agent",
                "purpose": "Generate a concise planning-oriented summary of likely demand shifts and associated risks.",
                "inputs": [
                    "Historical sales",
                    "Inventory positions",
                    "Seasonality signals",
                    "Promotion context",
                ],
                "pattern": "Combine trend signals -> detect anomalies -> summarize forecast implications",
            }
        )

    if "Reduce support load" in priorities:
        agents.append(
            {
                "name": "Support Volume Agent",
                "purpose": "Explain what is driving contact volume and identify the most valuable reduction opportunities.",
                "inputs": [
                    "Ticket text",
                    "Ticket categories",
                    "Escalation data",
                    "Customer or product context",
                ],
                "pattern": "Classify contact reasons -> measure frequency and impact -> prioritize fixes",
            }
        )

    if "Improve promotion effectiveness" in priorities:
        agents.append(
            {
                "name": "Promotion Performance Agent",
                "purpose": "Explain which promotions are working, where performance differs, and what to change next.",
                "inputs": [
                    "Campaign data",
                    "Sales response",
                    "Product attributes",
                    "Segment performance",
                ],
                "pattern": "Compare campaigns -> identify uplift drivers -> summarize recommendations",
            }
        )

    if not agents:
        agents.append(
            {
                "name": f"{industry} Insight Agent",
                "purpose": "Summarize priority operational patterns and recommend next actions from curated Snowflake data.",
                "inputs": [
                    "Curated business data",
                    "Relevant operational context",
                    "Stakeholder-defined priority metrics",
                ],
                "pattern": "Monitor -> summarize -> prioritize -> recommend",
            }
        )

    return agents[:3]


def clean_markdown_for_pdf(text: str) -> str:
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", text)
    text = text.replace("&", "&amp;")
    text = text.replace("<b>", "%%B%%").replace("</b>", "%%/B%%")
    text = text.replace("<i>", "%%I%%").replace("</i>", "%%/I%%")
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    text = text.replace("%%B%%", "<b>").replace("%%/B%%", "</b>")
    text = text.replace("%%I%%", "<i>").replace("%%/I%%", "</i>")
    return text


def build_pdf_bytes(
    customer_name: str,
    industry: str,
    data_sources: list[str],
    bi_tool: str,
    refresh_cadence: str,
    priorities: list[str],
    unstructured_data: list[str],
    fiscal_timing: str,
    additional_context: str,
    summary: str,
    architecture: str,
    mvps: list[dict[str, Any]],
    roadmap: list[dict[str, Any]],
    handover: str,
    agents: list[dict[str, Any]],
    enhanced_output: str | None = None,
) -> bytes:
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=22 * mm,
        bottomMargin=18 * mm,
        title=f"AI Activation Plan - {customer_name}",
        author="AI Activation Copilot",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=28,
        textColor=colors.HexColor("#16324f"),
        alignment=TA_LEFT,
        spaceAfter=14,
    )

    sub_style = ParagraphStyle(
        "SubStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#5b6b7a"),
        spaceAfter=8,
    )

    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#2596be"),
        spaceBefore=14,
        spaceAfter=8,
    )

    subhead_style = ParagraphStyle(
        "Subhead",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor("#16324f"),
        spaceBefore=8,
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#243746"),
        spaceAfter=6,
    )

    story: list[Any] = []

    def add_paragraphs(text: str) -> None:
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        for paragraph in paragraphs:
            story.append(Paragraph(clean_markdown_for_pdf(paragraph).replace("\n", "<br/>"), body_style))

    def add_bullets(items: list[str]) -> None:
        if not items:
            return
        story.append(
            ListFlowable(
                [ListItem(Paragraph(clean_markdown_for_pdf(i), body_style)) for i in items],
                bulletType="bullet",
                leftIndent=14,
            )
        )
        story.append(Spacer(1, 6))

    story.append(Paragraph("AI Activation Copilot", title_style))
    story.append(Paragraph(f"{customer_name} – {industry} – 90-Day Activation Blueprint", sub_style))
    story.append(Paragraph("Prepared for customer discussion and activation planning", sub_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Customer Inputs", section_style))
    add_bullets(
        [
            f"Industry: {industry}",
            f"Primary data sources: {_fmt_list(data_sources)}",
            f"Primary BI tool: {bi_tool}",
            f"Operational refresh cadence: {refresh_cadence}",
            f"Unstructured data available: {_fmt_list(unstructured_data)}",
            f"Business priorities: {_fmt_list(priorities)}",
            f"Fiscal timing: {fiscal_timing}",
        ]
    )

    if additional_context.strip():
        story.append(Paragraph("Discovery Notes for AI Refinement", section_style))
        add_paragraphs(additional_context)
        story.append(Spacer(1, 4))

    story.append(Paragraph("Activation Summary", section_style))
    add_paragraphs(summary)

    story.append(Paragraph("Recommended Architecture", section_style))
    add_paragraphs(architecture)

    story.append(Paragraph("Thin-Slice MVPs", section_style))
    if mvps:
        for mvp in mvps:
            story.append(Paragraph(clean_markdown_for_pdf(mvp["title"]), subhead_style))
            add_bullets(
                [
                    f"Scope: {mvp['scope']}",
                    f"Why first: {mvp['why']}",
                    f"Business outcome: {mvp['outcome']}",
                ]
            )
    else:
        story.append(Paragraph("No MVPs generated.", body_style))

    story.append(Paragraph("30-60-90 Activation Plan", section_style))
    for phase in roadmap:
        story.append(Paragraph(clean_markdown_for_pdf(phase["phase"]), subhead_style))
        items: list[str] = []
        items.extend([f"Objective: {item}" for item in phase["objectives"]])
        items.extend([f"Deliverable: {item}" for item in phase["deliverables"]])
        items.extend([f"Team impacted: {item}" for item in phase["teams"]])
        add_bullets(items)

    story.append(Paragraph("Day 90 Handover", section_style))
    add_paragraphs(handover)

    story.append(Paragraph("Suggested Agent Templates", section_style))
    if agents:
        for agent in agents:
            story.append(Paragraph(clean_markdown_for_pdf(agent["name"]), subhead_style))
            add_bullets(
                [
                    f"Purpose: {agent['purpose']}",
                    f"Inputs: {', '.join(agent['inputs'])}",
                    f"Pattern: {agent['pattern']}",
                ]
            )
    else:
        story.append(Paragraph("No agent templates generated.", body_style))

    if enhanced_output:
        story.append(Paragraph("AI-Enhanced Activation Blueprint", section_style))
        add_paragraphs(enhanced_output)

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def _serialize_for_prompt(value: Any) -> str:
    try:
        return json.dumps(value, indent=2, ensure_ascii=False)
    except Exception:
        return str(value)


def enhance_plan_with_llm(
    api_key: str,
    customer_name: str,
    industry: str,
    data_sources: list[str],
    bi_tool: str,
    refresh_cadence: str,
    priorities: list[str],
    unstructured_data: list[str],
    fiscal_timing: str,
    additional_context: str,
    summary: str,
    architecture: str,
    mvps: list[dict[str, Any]],
    roadmap: list[dict[str, Any]],
    handover: str,
    agents: list[dict[str, Any]],
) -> str:
    client = OpenAI(api_key=api_key)

    system_prompt = """You are a senior Snowflake activation strategist.

Your job is to refine a draft 90-day customer activation blueprint into a sharper, more executive-ready version.

Requirements:
- Keep recommendations practical and commercially grounded.
- Make the output sound like a customer-facing activation plan, not internal notes.
- Strengthen the plan with explicit risks, dependencies, success metrics, and talk track ideas.
- Use the additional customer discovery notes if provided.
- Do not invent niche technical specifics unless supported by the input.
- Be concise but substantive.
- Format the response in markdown.

Use the following exact structure:

## Executive Framing
A concise paragraph explaining what the customer needs and how the activation should be framed.

## Recommended Activation Posture
3-5 bullets.

## Refined MVP Recommendations
For each MVP, provide:
### [MVP name]
- What to deliver
- Why it matters now
- Risk or dependency
- Success metric

## Key Delivery Risks and Mitigations
4-6 bullets.

## Day 90 Success Measures
4-6 bullets.

## Customer Talk Track
A short set of bullets that an account engineer could say to the customer.

## Recommended Next-Step Expansion
A concise paragraph on what should come after the initial 90 days.
"""

    user_prompt = f"""
Customer name: {customer_name}
Industry: {industry}
Primary data sources: {_fmt_list(data_sources)}
Primary BI tool: {bi_tool}
Operational refresh cadence: {refresh_cadence}
Business priorities: {_fmt_list(priorities)}
Unstructured data available: {_fmt_list(unstructured_data)}
Fiscal timing: {fiscal_timing}

Additional customer context:
{additional_context.strip() if additional_context.strip() else "None provided."}

Draft activation summary:
{summary}

Draft architecture:
{architecture}

Draft MVPs:
{_serialize_for_prompt(mvps)}

Draft roadmap:
{_serialize_for_prompt(roadmap)}

Draft handover:
{handover}

Draft agent templates:
{_serialize_for_prompt(agents)}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.output_text.strip()

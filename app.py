import re
from io import BytesIO

import streamlit as st
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer
from utils import (
    generate_activation_summary,
    generate_architecture,
    generate_mvps,
    generate_roadmap,
    generate_handover,
    generate_agent_templates,
    enhance_plan_with_llm,
)

BRAND_BLUE = "#2596be"
BRAND_BLUE_DARK = "#1f84a7"
BG = "#f4f7fb"
CARD_BG = "#ffffff"
TEXT = "#1f2937"
MUTED = "#6b7280"
BORDER = "#d9e2ec"


st.set_page_config(
    page_title="AI Activation Copilot",
    page_icon="❄️",
    layout="wide",
)


st.markdown(
    f"""
    <style>
    .stApp {{
        background: {BG};
    }}

    .block-container {{
        max-width: 1240px;
        padding-top: 1.25rem;
        padding-bottom: 2rem;
    }}

    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #f7f9fc 0%, #eef4f8 100%);
        border-right: 1px solid rgba(15, 23, 42, 0.06);
    }}

    section[data-testid="stSidebar"] .block-container {{
        padding-top: 1rem;
    }}

    h1, h2, h3, h4, h5, h6 {{
        color: {TEXT};
        letter-spacing: -0.02em;
    }}

    p, label, div, span {{
        color: {TEXT};
    }}

    .hero-card {{
        padding: 1.35rem 1.4rem;
        border: 1px solid {BORDER};
        border-radius: 20px;
        background: linear-gradient(135deg, #ffffff 0%, #f8fbfd 100%);
        box-shadow: 0 10px 30px rgba(37, 150, 190, 0.08);
        margin-bottom: 1rem;
    }}

    .content-card {{
        background: {CARD_BG};
        border: 1px solid {BORDER};
        border-radius: 18px;
        padding: 1.2rem 1.2rem 0.9rem 1.2rem;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.04);
        margin-bottom: 1rem;
    }}

    .content-card h3 {{
        margin-top: 0;
        margin-bottom: 0.8rem;
    }}

    div[data-testid="metric-container"] {{
        background: {CARD_BG};
        border: 1px solid {BORDER};
        padding: 0.85rem 1rem;
        border-radius: 16px;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.04);
    }}

    div[data-testid="metric-container"] label {{
        color: {MUTED} !important;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background: transparent;
        padding: 0.2rem;
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 46px;
        border-radius: 14px;
        padding-left: 16px;
        padding-right: 16px;
        background: rgba(255,255,255,0.7);
        border: 1px solid {BORDER};
    }}

    .stTabs [aria-selected="true"] {{
        background: rgba(37,150,190,0.10) !important;
        border-color: rgba(37,150,190,0.35) !important;
    }}

    .stExpander {{
        border: 1px solid {BORDER} !important;
        border-radius: 16px !important;
        background: {CARD_BG} !important;
        overflow: hidden;
    }}

    .stButton > button[kind="primary"] {{
        background-color: {BRAND_BLUE} !important;
        border-color: {BRAND_BLUE} !important;
        color: white !important;
        border-radius: 14px !important;
        min-height: 3rem;
        font-weight: 600;
    }}

    .stButton > button[kind="primary"]:hover {{
        background-color: {BRAND_BLUE_DARK} !important;
        border-color: {BRAND_BLUE_DARK} !important;
        color: white !important;
    }}

    .stButton > button[kind="primary"]:focus {{
        box-shadow: 0 0 0 0.2rem rgba(37, 150, 190, 0.25) !important;
        outline: none !important;
    }}

    .stDownloadButton > button {{
        background-color: white !important;
        color: {TEXT} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 14px !important;
        min-height: 3rem;
        font-weight: 600;
        width: 100%;
    }}

    .stDownloadButton > button:hover {{
        border-color: {BRAND_BLUE} !important;
        color: {BRAND_BLUE} !important;
    }}

    [data-baseweb="tag"] {{
        background-color: {BRAND_BLUE} !important;
        border-color: {BRAND_BLUE} !important;
        color: white !important;
        border-radius: 999px !important;
    }}

    [data-baseweb="tag"] * {{
        color: white !important;
    }}

    div[data-baseweb="select"] > div {{
        border-radius: 14px !important;
        border: 1px solid {BORDER} !important;
        background: white !important;
        min-height: 54px;
    }}

    .stTextInput > div > div > input {{
        border-radius: 14px !important;
        border: 1px solid {BORDER} !important;
        background: white !important;
    }}

    .stTextArea textarea {{
        border-radius: 14px !important;
        border: 1px solid {BORDER} !important;
        background: white !important;
    }}

    .download-card {{
        padding: 1rem 1.1rem;
        border: 1px solid {BORDER};
        border-radius: 18px;
        background: linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
    }}

    .mini-note {{
        color: {MUTED};
        font-size: 0.92rem;
    }}

    .card-title {{
        font-weight: 700;
        margin-bottom: 0.35rem;
    }}

    .no-anchor a {{
        display: none !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


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


def paragraph_blocks(text: str):
    lines = [line.rstrip() for line in text.split("\n")]
    blocks = []
    current = []

    for line in lines:
        if not line.strip():
            if current:
                blocks.append("\n".join(current).strip())
                current = []
        else:
            current.append(line)

    if current:
        blocks.append("\n".join(current).strip())

    return blocks


def render_markdown_in_card(title: str, body: str):
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown(f"### {title}")
    st.markdown(body)
    st.markdown("</div>", unsafe_allow_html=True)


def build_pdf_bytes(
    customer_name,
    industry,
    data_sources,
    bi_tool,
    refresh_cadence,
    priorities,
    unstructured_data,
    fiscal_timing,
    additional_context,
    summary,
    architecture,
    mvps,
    roadmap,
    handover,
    agents,
    enhanced_output=None,
):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=20 * mm,
        bottomMargin=18 * mm,
        title=f"AI Activation Plan - {customer_name}",
        author="AI Activation Copilot",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=28,
        textColor=colors.HexColor("#16324f"),
        alignment=TA_LEFT,
        spaceAfter=8,
    )

    sub_style = ParagraphStyle(
        "SubStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#5b6b7a"),
        spaceAfter=14,
    )

    h1 = ParagraphStyle(
        "H1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=colors.HexColor(BRAND_BLUE),
        spaceBefore=10,
        spaceAfter=8,
    )

    h2 = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor("#16324f"),
        spaceBefore=8,
        spaceAfter=6,
    )

    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.8,
        leading=14,
        textColor=colors.HexColor("#243746"),
        spaceAfter=6,
    )

    bullet_style = ParagraphStyle(
        "BulletStyle",
        parent=body,
        leftIndent=8,
        firstLineIndent=0,
        spaceBefore=0,
        spaceAfter=2,
    )

    story = []

    story.append(Paragraph("AI Activation Copilot", title_style))
    story.append(Paragraph(f"{customer_name} - {industry} - 90-Day Activation Blueprint", sub_style))

    story.append(Paragraph("Customer Inputs", h1))
    inputs = [
        f"Industry: {industry}",
        f"Primary data sources: {', '.join(data_sources) if data_sources else 'None selected'}",
        f"Primary BI tool: {bi_tool}",
        f"Operational refresh cadence: {refresh_cadence}",
        f"Unstructured data available: {', '.join(unstructured_data) if unstructured_data else 'None selected'}",
        f"Business priorities: {', '.join(priorities) if priorities else 'None selected'}",
        f"Fiscal timing: {fiscal_timing}",
    ]
    story.append(
        ListFlowable(
            [ListItem(Paragraph(clean_markdown_for_pdf(item), bullet_style)) for item in inputs],
            bulletType="bullet",
            leftIndent=14,
        )
    )
    story.append(Spacer(1, 8))

    if additional_context.strip():
        story.append(Paragraph("Discovery Notes for AI Refinement", h1))
        for block in paragraph_blocks(additional_context):
            story.append(Paragraph(clean_markdown_for_pdf(block).replace("\n", "<br/>"), body))
        story.append(Spacer(1, 4))

    def add_text_section(title, text):
        story.append(Paragraph(title, h1))
        for block in paragraph_blocks(text):
            story.append(Paragraph(clean_markdown_for_pdf(block).replace("\n", "<br/>"), body))
        story.append(Spacer(1, 4))

    add_text_section("Activation Summary", summary)
    add_text_section("Recommended Architecture", architecture)

    story.append(Paragraph("Thin-Slice MVPs", h1))
    if mvps:
        for mvp in mvps:
            story.append(Paragraph(clean_markdown_for_pdf(mvp["title"]), h2))
            items = [
                f"<b>Scope:</b> {mvp['scope']}",
                f"<b>Why first:</b> {mvp['why']}",
                f"<b>Business outcome:</b> {mvp['outcome']}",
            ]
            story.append(
                ListFlowable(
                    [ListItem(Paragraph(clean_markdown_for_pdf(item), bullet_style)) for item in items],
                    bulletType="bullet",
                    leftIndent=14,
                )
            )
            story.append(Spacer(1, 4))
    else:
        story.append(Paragraph("No MVPs generated.", body))

    story.append(Paragraph("30-60-90 Activation Plan", h1))
    for phase in roadmap:
        story.append(Paragraph(clean_markdown_for_pdf(phase["phase"]), h2))
        phase_items = []
        phase_items.extend([f"<b>Objective:</b> {item}" for item in phase["objectives"]])
        phase_items.extend([f"<b>Deliverable:</b> {item}" for item in phase["deliverables"]])
        phase_items.extend([f"<b>Team impacted:</b> {item}" for item in phase["teams"]])

        story.append(
            ListFlowable(
                [ListItem(Paragraph(clean_markdown_for_pdf(item), bullet_style)) for item in phase_items],
                bulletType="bullet",
                leftIndent=14,
            )
        )
        story.append(Spacer(1, 4))

    add_text_section("Day 90 Handover", handover)

    story.append(Paragraph("Suggested Agent Templates", h1))
    if agents:
        for agent in agents:
            story.append(Paragraph(clean_markdown_for_pdf(agent["name"]), h2))
            agent_items = [
                f"<b>Purpose:</b> {agent['purpose']}",
                f"<b>Inputs:</b> {', '.join(agent['inputs'])}",
                f"<b>Pattern:</b> {agent['pattern']}",
            ]
            story.append(
                ListFlowable(
                    [ListItem(Paragraph(clean_markdown_for_pdf(item), bullet_style)) for item in agent_items],
                    bulletType="bullet",
                    leftIndent=14,
                )
            )
            story.append(Spacer(1, 4))
    else:
        story.append(Paragraph("No agent templates generated.", body))

    if enhanced_output:
        add_text_section("AI-Enhanced Activation Blueprint", enhanced_output)

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


st.title("AI Activation Copilot")
st.caption("Generate a 90-day Snowflake activation blueprint from customer discovery inputs.")

if "plan_generated" not in st.session_state:
    st.session_state.plan_generated = False

if "enhanced_output" not in st.session_state:
    st.session_state.enhanced_output = None

if "last_plan_signature" not in st.session_state:
    st.session_state.last_plan_signature = None


with st.sidebar:
    st.header("Customer Inputs")
    st.markdown(
        """
        <div class="mini-note">
        Capture the customer landscape, priorities, stakeholder context, and delivery constraints, then generate a structured activation blueprint.
        </div>
        """,
        unsafe_allow_html=True,
    )

    customer_name = st.text_input("Customer name", value="RetailCo")

    industry = st.selectbox(
        "Industry",
        ["Retail", "Financial Services", "Manufacturing", "Healthcare", "Other"],
        index=0,
    )

    data_sources = st.multiselect(
        "Primary data sources",
        ["MySQL", "Postgres", "SQL Server", "Redshift", "BigQuery", "S3", "APIs", "Salesforce"],
        default=["MySQL", "Redshift"],
    )

    bi_tool = st.selectbox(
        "Primary BI tool",
        ["Tableau", "Power BI", "Looker", "Excel", "Other"],
        index=0,
    )

    refresh_cadence = st.selectbox(
        "Operational refresh cadence",
        ["Real-time", "15 minutes", "Hourly", "Daily"],
        index=1,
    )

    unstructured_data = st.multiselect(
        "Unstructured data available",
        ["Product reviews", "Support tickets", "Return reasons", "Chat transcripts", "Emails"],
        default=["Product reviews", "Support tickets", "Return reasons"],
    )

    priorities = st.multiselect(
        "Business priorities",
        [
            "Reduce stockouts",
            "Improve customer sentiment insight",
            "Increase conversion",
            "Improve forecasting",
            "Reduce support load",
            "Improve promotion effectiveness",
        ],
        default=["Reduce stockouts", "Improve customer sentiment insight", "Increase conversion"],
    )

    fiscal_timing = st.selectbox(
        "Customer position in fiscal cycle",
        ["Near end of quarter/year", "Good time left in fiscal year"],
        index=1,
    )

    additional_context = st.text_area(
        "Discovery notes for AI refinement",
        value="",
        height=140,
        placeholder=(
            "Example: Customer wants executive-visible value in 30 days. "
            "Small data team. Legacy migration is politically sensitive. "
            "Support tickets are messy and uncategorized."
        ),
    )

    if st.button("Generate Activation Plan", type="primary", use_container_width=True):
        st.session_state.plan_generated = True


if not st.session_state.plan_generated:
    st.markdown(
        """
        <div class="hero-card">
            <h3 style="margin-top:0; margin-bottom:0.4rem;">Build a customer-ready activation plan</h3>
            <p style="margin-bottom:0.6rem; color:#475467;">
                Enter discovery inputs in the sidebar, generate a deterministic activation blueprint,
                then optionally refine it with AI using richer customer notes.
            </p>
            <p style="margin-bottom:0; color:#667085;">
                Includes customer summary, architecture recommendation, thin-slice MVPs, 30-60-90 roadmap,
                handover guidance, agent ideas, and export to PDF.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()


summary = generate_activation_summary(
    customer_name=customer_name,
    industry=industry,
    data_sources=data_sources,
    bi_tool=bi_tool,
    refresh_cadence=refresh_cadence,
    priorities=priorities,
    unstructured_data=unstructured_data,
)

architecture = generate_architecture(
    industry=industry,
    data_sources=data_sources,
    refresh_cadence=refresh_cadence,
    bi_tool=bi_tool,
    unstructured_data=unstructured_data,
)

mvps = generate_mvps(
    industry=industry,
    priorities=priorities,
    unstructured_data=unstructured_data,
)

roadmap = generate_roadmap(
    industry=industry,
    priorities=priorities,
    refresh_cadence=refresh_cadence,
    unstructured_data=unstructured_data,
)

handover = generate_handover(fiscal_timing=fiscal_timing)

agents = generate_agent_templates(
    industry=industry,
    priorities=priorities,
)

plan_signature = (
    customer_name,
    industry,
    tuple(sorted(data_sources)),
    bi_tool,
    refresh_cadence,
    tuple(sorted(unstructured_data)),
    tuple(sorted(priorities)),
    fiscal_timing,
    additional_context,
)

if st.session_state.last_plan_signature != plan_signature:
    st.session_state.enhanced_output = None
    st.session_state.last_plan_signature = plan_signature


m1, m2, m3, m4 = st.columns(4)
m1.metric("Industry", industry)
m2.metric("BI Tool", bi_tool)
m3.metric("Refresh", refresh_cadence)
m4.metric("Priority Count", len(priorities))

tab1, tab2, tab3, tab4 = st.tabs(
    ["Overview", "Thin-Slice MVPs", "30-60-90 Plan", "Handover & Agents"]
)

with tab1:
    left, right = st.columns(2)
    with left:
        render_markdown_in_card("Activation Summary", summary)
    with right:
        render_markdown_in_card("Recommended Architecture", architecture)

with tab2:
    st.subheader("Thin-Slice MVPs")
    if mvps:
        for mvp in mvps:
            with st.expander(mvp["title"], expanded=True):
                st.markdown(f"**Scope:** {mvp['scope']}")
                st.markdown(f"**Why first:** {mvp['why']}")
                st.markdown(f"**Business outcome:** {mvp['outcome']}")
    else:
        st.warning("No MVPs were generated. Select at least one business priority.")

with tab3:
    st.subheader("30-60-90 Activation Plan")
    for phase in roadmap:
        with st.expander(phase["phase"], expanded=True):
            st.markdown("**Objectives**")
            for item in phase["objectives"]:
                st.markdown(f"- {item}")

            st.markdown("**Deliverables**")
            for item in phase["deliverables"]:
                st.markdown(f"- {item}")

            st.markdown("**Customer teams impacted**")
            for item in phase["teams"]:
                st.markdown(f"- {item}")

with tab4:
    left, right = st.columns(2)
    with left:
        render_markdown_in_card("Day 90 Handover", handover)
    with right:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### Suggested Agent Templates")
        if agents:
            for agent in agents:
                with st.expander(agent["name"], expanded=False):
                    st.markdown(f"**Purpose:** {agent['purpose']}")
                    st.markdown("**Inputs:**")
                    for item in agent["inputs"]:
                        st.markdown(f"- {item}")
                    st.markdown(f"**Pattern:** {agent['pattern']}")
        else:
            st.info("No agent templates were generated for the selected priorities.")
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.subheader("AI Enhancement")

try:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    ai_key_available = True
except Exception:
    openai_api_key = None
    ai_key_available = False

if additional_context.strip():
    st.info("Discovery notes will be included in the AI refinement prompt.")

if not ai_key_available:
    st.info("Add OPENAI_API_KEY in Streamlit secrets to enable AI enhancement.")

if st.button("Enhance with AI", type="primary", use_container_width=True, disabled=not ai_key_available):
    try:
        with st.spinner("Generating AI-enhanced activation blueprint..."):
            st.session_state.enhanced_output = enhance_plan_with_llm(
                api_key=openai_api_key,
                customer_name=customer_name,
                industry=industry,
                data_sources=data_sources,
                bi_tool=bi_tool,
                refresh_cadence=refresh_cadence,
                priorities=priorities,
                unstructured_data=unstructured_data,
                fiscal_timing=fiscal_timing,
                additional_context=additional_context,
                summary=summary,
                architecture=architecture,
                mvps=mvps,
                roadmap=roadmap,
                handover=handover,
                agents=agents,
            )
    except Exception as e:
        st.error(f"AI enhancement failed: {e}")

if st.session_state.enhanced_output:
    st.divider()
    st.subheader("AI-Enhanced Activation Blueprint")
    st.markdown(st.session_state.enhanced_output)

plan_pdf = build_pdf_bytes(
    customer_name=customer_name,
    industry=industry,
    data_sources=data_sources,
    bi_tool=bi_tool,
    refresh_cadence=refresh_cadence,
    priorities=priorities,
    unstructured_data=unstructured_data,
    fiscal_timing=fiscal_timing,
    additional_context=additional_context,
    summary=summary,
    architecture=architecture,
    mvps=mvps,
    roadmap=roadmap,
    handover=handover,
    agents=agents,
    enhanced_output=st.session_state.enhanced_output,
)

st.divider()
st.subheader("Export Customer Activation Blueprint")

st.markdown(
    """
    <div class="download-card">
        <div class="card-title">Download a customer-ready PDF</div>
        <div class="mini-note" style="margin-bottom:0.9rem;">
            Export the full blueprint including discovery inputs, deterministic plan content,
            and any AI-refined output.
        </div>
    """,
    unsafe_allow_html=True,
)

st.download_button(
    label="Download Activation Plan (PDF)",
    data=plan_pdf,
    file_name=f"{customer_name.lower().replace(' ', '_')}_activation_plan.pdf",
    mime="application/pdf",
    use_container_width=True,
)

st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.caption(
    "This prototype generates a deterministic activation blueprint first, then optionally uses an LLM to sharpen recommendations, risks, success metrics, and customer talk track using structured inputs plus discovery notes."
)

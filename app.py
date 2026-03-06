import streamlit as st
from utils import (
    generate_activation_summary,
    generate_architecture,
    generate_mvps,
    generate_roadmap,
    generate_handover,
    generate_agent_templates,
    enhance_plan_with_llm,
)

st.set_page_config(
    page_title="AI Activation Copilot",
    page_icon="❄️",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .hero-card {
        padding: 1.2rem 1.4rem;
        border: 1px solid rgba(128,128,128,0.18);
        border-radius: 18px;
        background: rgba(255,255,255,0.03);
        margin-bottom: 1rem;
    }

    .metric-card {
        padding: 0.9rem 1rem;
        border: 1px solid rgba(128,128,128,0.15);
        border-radius: 14px;
        background: rgba(255,255,255,0.02);
        text-align: center;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 44px;
        border-radius: 12px;
        padding-left: 16px;
        padding-right: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("AI Activation Copilot")
st.caption("Generate a 90-day Snowflake activation blueprint from customer discovery inputs.")

with st.sidebar:
    st.header("Customer Inputs")

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

    generate = st.button("Generate Activation Plan", type="primary", use_container_width=True)

if not generate:
    st.markdown(
        """
        <div class="hero-card">
            <h4 style="margin-top:0;">How it works</h4>
            <p style="margin-bottom:0;">
                Enter discovery inputs in the sidebar, then click <b>Generate Activation Plan</b>.
                The copilot will produce a customer summary, recommended architecture, thin-slice MVPs,
                a 30-60-90 roadmap, handover guidance, and agent ideas.
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
    priorities=priorities,
    refresh_cadence=refresh_cadence,
    unstructured_data=unstructured_data,
)

handover = generate_handover(fiscal_timing=fiscal_timing)

agents = generate_agent_templates(
    industry=industry,
    priorities=priorities,
)

# Top summary strip
m1, m2, m3, m4 = st.columns(4)
m1.metric("Industry", industry)
m2.metric("BI Tool", bi_tool)
m3.metric("Refresh", refresh_cadence)
m4.metric("Priority Count", len(priorities))

tab1, tab2, tab3, tab4 = st.tabs(
    ["Overview", "Thin-Slice MVPs", "30-60-90 Plan", "Handover & Agents"]
)

with tab1:
    left, right = st.columns([1, 1])

    with left:
        st.subheader("Activation Summary")
        st.markdown(summary)

    with right:
        st.subheader("Recommended Architecture")
        st.markdown(architecture)

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
    left, right = st.columns([1, 1])

    with left:
        st.subheader("Day 90 Handover")
        st.markdown(handover)

    with right:
        st.subheader("Suggested Agent Templates")
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

st.divider()

# AI enhancement section
st.subheader("AI Enhancement")

ai_key_available = "OPENAI_API_KEY" in st.secrets

if not ai_key_available:
    st.info("Add OPENAI_API_KEY in Streamlit secrets to enable AI enhancement.")

if st.button("Enhance with AI", use_container_width=True, disabled=not ai_key_available):
    try:
        with st.spinner("Generating AI-enhanced activation blueprint..."):
            enhanced_output = enhance_plan_with_llm(
                api_key=st.secrets["OPENAI_API_KEY"],
                customer_name=customer_name,
                industry=industry,
                data_sources=data_sources,
                bi_tool=bi_tool,
                refresh_cadence=refresh_cadence,
                priorities=priorities,
                unstructured_data=unstructured_data,
                fiscal_timing=fiscal_timing,
                summary=summary,
                architecture=architecture,
                mvps=mvps,
                roadmap=roadmap,
                handover=handover,
                agents=agents,
            )

        st.markdown(enhanced_output)

    except Exception as e:
        st.error(f"AI enhancement failed: {e}")

st.divider()
st.caption(
    "This prototype generates a deterministic activation blueprint first, then optionally uses an LLM to improve phrasing and presentation quality."
)
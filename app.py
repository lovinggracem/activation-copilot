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

    /* Fjord blue buttons */
    .stButton > button[kind="primary"] {
        background-color: #2596be !important;
        border-color: #2596be !important;
        color: white !important;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #1f84a7 !important;
        border-color: #1f84a7 !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

st.title("AI Activation Copilot")
st.caption("Generate a 90-day Snowflake activation blueprint from customer discovery inputs.")

if "plan_generated" not in st.session_state:
    st.session_state.plan_generated = False

if "enhanced_output" not in st.session_state:
    st.session_state.enhanced_output = None

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

    if st.button("Generate Activation Plan", type="primary", use_container_width=True):
        st.session_state.plan_generated = True


if not st.session_state.plan_generated:

    st.markdown(
        """
        <div class="hero-card">
        <h4>How it works</h4>
        Enter discovery inputs and generate a full 90-day Snowflake activation plan.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.stop()


summary = generate_activation_summary(
    customer_name,
    industry,
    data_sources,
    bi_tool,
    refresh_cadence,
    priorities,
    unstructured_data,
)

architecture = generate_architecture(
    industry,
    data_sources,
    refresh_cadence,
    bi_tool,
    unstructured_data,
)

mvps = generate_mvps(
    industry,
    priorities,
    unstructured_data,
)

roadmap = generate_roadmap(
    industry,
    priorities,
    refresh_cadence,
    unstructured_data,
)

handover = generate_handover(fiscal_timing)

agents = generate_agent_templates(
    industry,
    priorities,
)

tab1, tab2, tab3, tab4 = st.tabs(
    ["Overview", "Thin-Slice MVPs", "30-60-90 Plan", "Handover & Agents"]
)

with tab1:

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Activation Summary")
        st.markdown(summary)

    with col2:
        st.subheader("Recommended Architecture")
        st.markdown(architecture)


with tab2:

    st.subheader("Thin-Slice MVPs")

    for mvp in mvps:
        with st.expander(mvp["title"], expanded=True):

            st.markdown(f"**Scope:** {mvp['scope']}")
            st.markdown(f"**Why first:** {mvp['why']}")
            st.markdown(f"**Outcome:** {mvp['outcome']}")


with tab3:

    st.subheader("30-60-90 Plan")

    for phase in roadmap:

        with st.expander(phase["phase"], expanded=True):

            st.markdown("**Objectives**")

            for o in phase["objectives"]:
                st.markdown(f"- {o}")

            st.markdown("**Deliverables**")

            for d in phase["deliverables"]:
                st.markdown(f"- {d}")


with tab4:

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Day 90 Handover")
        st.markdown(handover)

    with col2:
        st.subheader("Agent Templates")

        for agent in agents:
            with st.expander(agent["name"]):

                st.markdown(f"**Purpose:** {agent['purpose']}")

                st.markdown("**Inputs**")

                for i in agent["inputs"]:
                    st.markdown(f"- {i}")

                st.markdown(f"**Pattern:** {agent['pattern']}")


st.divider()
st.subheader("AI Enhancement")

try:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    ai_key_available = True
except:
    ai_key_available = False


if st.button("Enhance with AI", type="primary", use_container_width=True, disabled=not ai_key_available):

    with st.spinner("Generating AI enhanced plan..."):

        st.session_state.enhanced_output = enhance_plan_with_llm(
            openai_api_key,
            customer_name,
            industry,
            data_sources,
            bi_tool,
            refresh_cadence,
            priorities,
            unstructured_data,
            fiscal_timing,
            summary,
            architecture,
            mvps,
            roadmap,
            handover,
            agents,
        )


# Build export text

plan_text = f"""

# AI Activation Plan

## Activation Summary
{summary}

## Architecture
{architecture}

## MVPs
{mvps}

## Roadmap
{roadmap}

## Handover
{handover}

"""


st.divider()
st.subheader("Download Plan")

st.download_button(
    label="Download Activation Plan",
    data=plan_text,
    file_name="activation_plan.md",
    mime="text/markdown",
)


if st.session_state.enhanced_output:

    st.divider()
    st.subheader("AI Enhanced Blueprint")

    st.markdown(st.session_state.enhanced_output)

    st.download_button(
        label="Download AI Enhanced Plan",
        data=st.session_state.enhanced_output,
        file_name="activation_plan_ai.md",
        mime="text/markdown",
    )

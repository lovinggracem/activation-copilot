import streamlit as st
from utils import (
    generate_activation_summary,
    generate_architecture,
    generate_mvps,
    generate_roadmap,
    generate_handover,
    generate_agent_templates,
)


st.set_page_config(
    page_title="AI Activation Copilot",
    page_icon="❄️",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        max-width: 1400px;
        margin: 0 auto;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
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
    st.info("Enter customer details in the sidebar, then click **Generate Activation Plan**.")
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


tab1, tab2, tab3 = st.tabs(["Summary", "Roadmap", "Agents"])

with tab1:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("1. Activation Summary")
        st.markdown(summary)

        st.subheader("2. Recommended Architecture")
        st.markdown(architecture)

    with col2:
        st.subheader("3. Thin-Slice MVPs")
        if mvps:
            for mvp in mvps:
                with st.expander(mvp["title"], expanded=True):
                    st.markdown(f"**Scope:** {mvp['scope']}")
                    st.markdown(f"**Why first:** {mvp['why']}")
                    st.markdown(f"**Business outcome:** {mvp['outcome']}")
        else:
            st.warning("No MVPs were generated. Select at least one business priority.")

with tab2:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("4. 30-60-90 Roadmap")
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

    with col2:
        st.subheader("5. Day 90 Handover")
        st.markdown(handover)

with tab3:
    st.subheader("6. Suggested Agent Templates")
    if agents:
        for agent in agents:
            with st.expander(agent["name"], expanded=True):
                st.markdown(f"**Purpose:** {agent['purpose']}")
                st.markdown("**Inputs:**")
                for item in agent["inputs"]:
                    st.markdown(f"- {item}")
                st.markdown(f"**Pattern:** {agent['pattern']}")
    else:
        st.info("No agent templates were generated for the selected priorities.")

st.divider()
st.caption(
    "Demo note: this prototype uses deterministic rules to generate a customer activation blueprint. "
    "It can be extended with an LLM for richer plan generation later."
)

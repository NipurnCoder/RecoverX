import streamlit as st
import pandas as pd
import plotly.express as px
import sys

sys.path.append(".")

from backend.recovery_engine import RecoveryEngine


st.set_page_config(
    page_title="RecoverX",
    page_icon="💰",
    layout="wide"
)


st.title("💰 RecoverX")
st.caption(
    "AI Revenue Recovery Agent — "
    "Detect. Decide. Recover."
)


@st.cache_data
def load_data():

    transactions = pd.read_csv(
        "data/transactions.csv"
    )

    customers = pd.read_csv(
        "data/customers.csv"
    )

    results = pd.read_csv(
        "data/recovery_results.csv"
    )

    return (
        transactions,
        customers,
        results
    )


transactions, customers, results = load_data()


failed = transactions[
    transactions["status"] == "FAILED"
]


# ======================================
# METRICS
# ======================================

revenue_at_risk = failed["amount"].sum()

expected_recoverable = (
    results[
        "expected_recoverable_revenue"
    ].sum()
)

recovered = (
    results[
        "recovered_revenue"
    ].sum()
)

recovery_rate = (
    recovered / revenue_at_risk * 100
    if revenue_at_risk > 0
    else 0
)


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "💸 Revenue At Risk",
    f"₹{revenue_at_risk:,.0f}"
)

col2.metric(
    "🎯 Expected Recoverable",
    f"₹{expected_recoverable:,.0f}"
)

col3.metric(
    "💰 Revenue Recovered",
    f"₹{recovered:,.0f}"
)

col4.metric(
    "📈 Recovery Rate",
    f"{recovery_rate:.1f}%"
)


st.divider()


# ======================================
# SIDEBAR
# ======================================

st.sidebar.title("RecoverX Control")

page = st.sidebar.radio(
    "Navigate",
    [
        "Command Center",
        "Recovery Queue",
        "Agent Decisions",
        "Analytics"
    ]
)


# ======================================
# COMMAND CENTER
# ======================================

if page == "Command Center":

    st.header("Command Center")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "Revenue Recovery Funnel"
        )

        funnel_df = pd.DataFrame({
            "Stage": [
                "Revenue At Risk",
                "Expected Recoverable",
                "Recovered"
            ],
            "Amount": [
                revenue_at_risk,
                expected_recoverable,
                recovered
            ]
        })

        fig = px.funnel(
            funnel_df,
            y="Stage",
            x="Amount"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader(
            "Recovery Status"
        )

        status_counts = (
            results["status"]
            .value_counts()
            .reset_index()
        )

        status_counts.columns = [
            "Status",
            "Count"
        ]

        fig = px.pie(
            status_counts,
            names="Status",
            values="Count"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    st.subheader(
        "🔥 Highest Expected Recoveries"
    )

    top = results.sort_values(
        "expected_recoverable_revenue",
        ascending=False
    ).head(10)

    st.dataframe(
        top[
            [
                "transaction_id",
                "customer_id",
                "amount",
                "risk_score",
                "recovery_probability",
                "expected_recoverable_revenue",
                "status"
            ]
        ],
        use_container_width=True
    )


# ======================================
# RECOVERY QUEUE
# ======================================

elif page == "Recovery Queue":

    st.header(
        "🎯 Revenue Recovery Queue"
    )

    threshold = st.slider(
        "Minimum Expected Recoverable Revenue",
        0,
        50000,
        1000
    )

    queue = results[
        results[
            "expected_recoverable_revenue"
        ] >= threshold
    ]

    queue = queue.sort_values(
        "expected_recoverable_revenue",
        ascending=False
    )

    st.write(
        f"{len(queue)} recovery opportunities found."
    )

    st.dataframe(
        queue,
        use_container_width=True
    )


# ======================================
# AGENT DECISIONS
# ======================================

elif page == "Agent Decisions":

    st.header(
        "🧠 AI Agent Decisions"
    )

    transaction_id = st.selectbox(
        "Select Recovery Case",
        results["transaction_id"].tolist()
    )

    case = results[
        results["transaction_id"]
        == transaction_id
    ].iloc[0]

    st.subheader(
        f"Case: {transaction_id}"
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Amount",
        f"₹{case['amount']:,.0f}"
    )

    c2.metric(
        "Risk Score",
        f"{case['risk_score']:.0f}/100"
    )

    c3.metric(
        "Recovery Probability",
        f"{case['recovery_probability']*100:.1f}%"
    )


    st.divider()

    st.subheader("1️⃣ Root Cause")

    st.info(
        f"Cause: {case['root_cause.cause']}\n\n"
        f"Confidence: "
        f"{case['root_cause.confidence']*100:.1f}%\n\n"
        f"{case['root_cause.explanation']}"
    )


    st.subheader(
        "2️⃣ Recommended Intervention"
    )

    st.success(
        f"Action: {case['strategy.action']}\n\n"
        f"Reason: {case['strategy.reason']}"
    )


    st.subheader(
        "3️⃣ Policy Decision"
    )

    policy = case["policy.decision"]

    if policy == "ALLOW":

        st.success(
            f"✓ AUTO APPROVED\n\n"
            f"{case['policy.reason']}"
        )

    elif policy == "HUMAN_APPROVAL":

        st.warning(
            f"⚠ HUMAN APPROVAL REQUIRED\n\n"
            f"{case['policy.reason']}"
        )

    else:

        st.error(
            f"✕ BLOCKED\n\n"
            f"{case['policy.reason']}"
        )


    st.subheader(
        "4️⃣ Final Outcome"
    )

    if case["status"] == "RECOVERED":

        st.success(
            f"💰 ₹{case['recovered_revenue']:,.2f} "
            f"RECOVERED"
        )

    else:

        st.warning(
            f"Status: {case['status']}"
        )


# ======================================
# ANALYTICS
# ======================================

elif page == "Analytics":

    st.header(
        "📊 Recovery Analytics"
    )

    col1, col2 = st.columns(2)

    with col1:

        failure_df = (
            failed.groupby(
                "failure_reason"
            )["amount"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            failure_df,
            x="failure_reason",
            y="amount",
            title="Revenue At Risk by Failure"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        recovered_df = (
            results.groupby(
                "strategy.action"
            )["recovered_revenue"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            recovered_df,
            x="strategy.action",
            y="recovered_revenue",
            title="Recovered Revenue by Strategy"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader(
        "Recovery Statistics"
    )

    st.dataframe(
        results.describe(),
        use_container_width=True
    )
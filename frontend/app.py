import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="RecoverX AI",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# SESSION STATE
# =========================================================

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

if "executed_cases" not in st.session_state:
    st.session_state.executed_cases = set()

if "audit_events" not in st.session_state:
    st.session_state.audit_events = []

if "analysis_runs" not in st.session_state:
    st.session_state.analysis_runs = 1


# =========================================================
# THEME
# =========================================================

dark_mode = st.session_state.theme == "Dark"

if dark_mode:

    BG = "#07111F"
    CARD = "#0D1B2A"
    CARD2 = "#112438"
    TEXT = "#F4F7FB"
    MUTED = "#91A4B8"
    BORDER = "#20354A"

    CYAN = "#19D3C5"
    VIOLET = "#8B7CFF"
    CORAL = "#FF6B6B"
    AMBER = "#FFC857"
    BLUE = "#4DA3FF"
    GREEN = "#2ED6A1"

else:

    BG = "#F5F7FB"
    CARD = "#FFFFFF"
    CARD2 = "#F0F4FA"
    TEXT = "#172033"
    MUTED = "#667085"
    BORDER = "#DCE3EC"

    CYAN = "#079B91"
    VIOLET = "#6558D3"
    CORAL = "#E45757"
    AMBER = "#D99A00"
    BLUE = "#2878D4"
    GREEN = "#159570"


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    f"""
<style>

html, body, [class*="css"] {{
    font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}}

.stApp {{
    background: {BG};
    color: {TEXT};
}}

section[data-testid="stSidebar"] {{
    background: linear-gradient(
        180deg,
        #081321 0%,
        #0C1B2D 55%,
        #101B2C 100%
    );
    border-right: 1px solid #20354A;
}}

section[data-testid="stSidebar"] * {{
    color: #DDE8F4 !important;
}}

.block-container {{
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}}

h1 {{
    font-size: 3rem !important;
    letter-spacing: -2px;
}}

h2 {{
    letter-spacing: -1px;
}}

.hero {{
    background:
        radial-gradient(circle at 90% 10%, rgba(25,211,197,.16), transparent 25%),
        radial-gradient(circle at 70% 80%, rgba(139,124,255,.12), transparent 30%),
        {CARD};
    border: 1px solid {BORDER};
    border-radius: 22px;
    padding: 30px;
    margin-bottom: 25px;
    box-shadow: 0 20px 50px rgba(0,0,0,.10);
}}

.eyebrow {{
    color: {CYAN};
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
}}

.hero-title {{
    font-size: 46px;
    font-weight: 800;
    line-height: 1.05;
    margin-top: 8px;
}}

.hero-subtitle {{
    color: {MUTED};
    font-size: 16px;
    margin-top: 12px;
}}

.status-pill {{
    display: inline-block;
    padding: 7px 13px;
    border-radius: 30px;
    background: rgba(25,211,197,.12);
    color: {CYAN};
    border: 1px solid rgba(25,211,197,.25);
    font-size: 12px;
    font-weight: 700;
}}

.metric-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 18px;
    padding: 20px;
    min-height: 125px;
    box-shadow: 0 12px 30px rgba(0,0,0,.08);
}}

.metric-label {{
    color: {MUTED};
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.metric-value {{
    color: {TEXT};
    font-size: 29px;
    font-weight: 800;
    margin-top: 8px;
}}

.metric-small {{
    color: {MUTED};
    font-size: 12px;
    margin-top: 4px;
}}

.section-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 20px;
    padding: 22px;
    margin-top: 18px;
}}

.ai-card {{
    background:
        linear-gradient(
            135deg,
            rgba(25,211,197,.08),
            rgba(139,124,255,.08)
        );
    border: 1px solid {BORDER};
    border-radius: 20px;
    padding: 24px;
}}

.chain {{
    border-left: 3px solid {CYAN};
    padding-left: 18px;
    margin: 14px 0;
}}

.chain-title {{
    font-weight: 800;
    color: {TEXT};
}}

.chain-text {{
    color: {MUTED};
    font-size: 13px;
    margin-top: 4px;
}}

.badge {{
    display: inline-block;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 800;
}}

.badge-green {{
    background: rgba(46,214,161,.13);
    color: {GREEN};
}}

.badge-red {{
    background: rgba(255,107,107,.13);
    color: {CORAL};
}}

.badge-yellow {{
    background: rgba(255,200,87,.14);
    color: {AMBER};
}}

.badge-blue {{
    background: rgba(77,163,255,.13);
    color: {BLUE};
}}

.kpi-line {{
    height: 7px;
    border-radius: 20px;
    background: {BORDER};
    margin-top: 8px;
}}

div[data-testid="stMetric"] {{
    background: {CARD};
    border: 1px solid {BORDER};
    padding: 15px;
    border-radius: 16px;
}}

.stButton > button {{
    border-radius: 12px;
    font-weight: 700;
    border: 1px solid {BORDER};
}}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# DATA
# =========================================================

@st.cache_data
def load_data():

    transactions = pd.read_csv("data/transactions.csv")
    customers = pd.read_csv("data/customers.csv")
    results = pd.read_csv("data/recovery_results.csv")

    return transactions, customers, results


transactions, customers, results = load_data()


# =========================================================
# SAFE COLUMN HELPER
# =========================================================

def col(df, name, default=None):

    if name in df.columns:
        return df[name]

    return pd.Series(
        [default] * len(df),
        index=df.index
    )


# =========================================================
# NORMALIZE DATA
# =========================================================

transactions["amount"] = pd.to_numeric(
    col(transactions, "amount", 0),
    errors="coerce"
).fillna(0)

results["amount"] = pd.to_numeric(
    col(results, "amount", 0),
    errors="coerce"
).fillna(0)

results["risk_score"] = pd.to_numeric(
    col(results, "risk_score", 0),
    errors="coerce"
).fillna(0)

results["recovery_probability"] = pd.to_numeric(
    col(results, "recovery_probability", 0),
    errors="coerce"
).fillna(0)

results["expected_recoverable_revenue"] = pd.to_numeric(
    col(results, "expected_recoverable_revenue", 0),
    errors="coerce"
).fillna(0)

results["recovered_revenue"] = pd.to_numeric(
    col(results, "recovered_revenue", 0),
    errors="coerce"
).fillna(0)


failed = transactions[
    transactions["status"].astype(str).str.upper() == "FAILED"
].copy()


# =========================================================
# CORE METRICS
# =========================================================

revenue_at_risk = failed["amount"].sum()

expected_recoverable = results[
    "expected_recoverable_revenue"
].sum()

recovered = results[
    "recovered_revenue"
].sum()

recovery_rate = (
    recovered / revenue_at_risk * 100
    if revenue_at_risk > 0
    else 0
)

failed_count = len(failed)

recovered_cases = len(
    results[
        results["status"].astype(str).str.upper()
        == "RECOVERED"
    ]
)

candidate_count = len(
    results[
        results["expected_recoverable_revenue"] > 0
    ]
)


# =========================================================
# PRIORITY SCORE
# =========================================================

results["priority_score"] = (
    results["expected_recoverable_revenue"]
    * (1 + results["recovery_probability"])
    * (1 + results["risk_score"] / 100)
)


ranked = results.sort_values(
    "priority_score",
    ascending=False
).reset_index(drop=True)


best = ranked.iloc[0]


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    """
<div style="
font-size:28px;
font-weight:800;
padding:10px 0 5px 0;
">
<span style="color:#19D3C5;">◆</span> Recover<span style="color:#FF6B6B;">X</span>
</div>
""",
    unsafe_allow_html=True
)

st.sidebar.caption(
    "AI Revenue Recovery Operating System"
)

st.sidebar.markdown("---")

theme_choice = st.sidebar.radio(
    "Appearance",
    ["Dark", "Light"],
    index=0 if dark_mode else 1
)

if theme_choice != st.session_state.theme:

    st.session_state.theme = theme_choice
    st.rerun()


page = st.sidebar.radio(
    "WORKSPACE",
    [
        "Command Center",
        "Transactions",
        "Recovery Queue",
        "Agent Decisions",
        "Policy Center",
        "Audit Trail",
        "Recovery Assistant",
        "Analytics"
    ]
)


st.sidebar.markdown("---")

st.sidebar.markdown(
    f"""
<div style="
background:#101F31;
padding:15px;
border-radius:14px;
border:1px solid #233A50;
">
<div style="font-size:11px;color:#91A4B8;">
ENVIRONMENT
</div>

<div style="
font-size:15px;
font-weight:700;
margin-top:5px;
">
Demo Workspace
</div>

<div style="
font-size:11px;
color:#91A4B8;
margin-top:4px;
">
Synthetic data • Simulation mode
</div>

<div style="
margin-top:12px;
color:#19D3C5;
font-size:11px;
">
● SYSTEM NOMINAL
</div>
</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# GLOBAL HERO
# =========================================================

st.markdown(
    f"""
<div class="hero">

<div class="eyebrow">
RECOVERX • AI REVENUE OPERATIONS
</div>

<div class="hero-title">
Revenue, recovered.
</div>

<div class="hero-subtitle">
Detect failed payments, understand why they failed,
choose the safest intervention, and track every decision.
</div>

<div style="margin-top:18px;">
<span class="status-pill">
● LIVE SIMULATION
</span>

<span style="margin-left:10px;color:{MUTED};font-size:12px;">
Analysis run #{st.session_state.analysis_runs}
</span>
</div>

</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# TOP METRICS
# =========================================================

m1, m2, m3, m4 = st.columns(4)


def metric_card(container, label, value, subtitle):

    container.markdown(
        f"""
<div class="metric-card">

<div class="metric-label">
{label}
</div>

<div class="metric-value">
{value}
</div>

<div class="metric-small">
{subtitle}
</div>

</div>
""",
        unsafe_allow_html=True
    )


metric_card(
    m1,
    "💸 Revenue At Risk",
    f"₹{revenue_at_risk:,.0f}",
    f"{failed_count:,} failed transactions"
)

metric_card(
    m2,
    "🎯 Recoverable Pool",
    f"₹{expected_recoverable:,.0f}",
    f"{candidate_count:,} candidates"
)

metric_card(
    m3,
    "💰 Revenue Recovered",
    f"₹{recovered:,.0f}",
    f"{recovered_cases:,} successful recoveries"
)

metric_card(
    m4,
    "📈 Recovery Rate",
    f"{recovery_rate:.1f}%",
    "Recovered / revenue at risk"
)


# =========================================================
# COMMAND CENTER
# =========================================================

if page == "Command Center":

    st.markdown("---")

    c1, c2 = st.columns([1.5, 1])

    with c1:

        st.subheader("⚡ Revenue Recovery Funnel")

        funnel_df = pd.DataFrame({
            "Stage": [
                "Revenue At Risk",
                "Expected Recoverable",
                "Revenue Recovered"
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

        fig.update_layout(
            paper_bgcolor=CARD,
            plot_bgcolor=CARD,
            font_color=TEXT,
            margin=dict(l=20, r=20, t=30, b=20)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with c2:

        st.subheader("🧠 Agent Health")

        health_items = [
            ("Risk Engine", "ONLINE", GREEN),
            ("Recovery Agent", "READY", CYAN),
            ("Policy Engine", "ACTIVE", VIOLET),
            ("Audit Logger", "TRACKING", AMBER)
        ]

        for name, status, color in health_items:

            st.markdown(
                f"""
<div style="
display:flex;
justify-content:space-between;
padding:13px 0;
border-bottom:1px solid {BORDER};
">

<div>{name}</div>

<div style="
color:{color};
font-weight:800;
font-size:12px;
">
● {status}
</div>

</div>
""",
                unsafe_allow_html=True
            )


    # -----------------------------------------------------
    # EXPOSURE MAP
    # -----------------------------------------------------

    st.markdown("### 🔥 Where the Money Is Stuck")

    if "failure_reason" in failed.columns:

        exposure = (
            failed.groupby("failure_reason")["amount"]
            .sum()
            .reset_index()
            .sort_values("amount", ascending=False)
        )

        for _, row in exposure.head(6).iterrows():

            percentage = (
                row["amount"] / revenue_at_risk * 100
                if revenue_at_risk
                else 0
            )

            st.markdown(
                f"""
<div style="margin:14px 0;">

<div style="
display:flex;
justify-content:space-between;
font-size:13px;
">

<span>{row['failure_reason']}</span>

<span style="font-weight:700;">
₹{row['amount']:,.0f}
</span>

</div>

<div class="kpi-line">

<div style="
width:{min(percentage,100):.1f}%;
height:7px;
border-radius:20px;
background:linear-gradient(
90deg,
{CORAL},
{AMBER}
);
">
</div>

</div>

</div>
""",
                unsafe_allow_html=True
            )


    # -----------------------------------------------------
    # NEXT BEST RECOVERY
    # -----------------------------------------------------

    st.markdown("### 🎯 Next Best Recovery")

    left, right = st.columns([1.4, 1])

    with left:

        st.markdown(
            f"""
<div class="ai-card">

<div class="eyebrow">
AI RECOMMENDATION
</div>

<h2>
{best.get("strategy.action", "RETRY")}
</h2>

<p style="color:{MUTED};">
{best.get("strategy.reason", "Highest expected recovery opportunity.")}
</p>

<div class="chain">

<div class="chain-title">
Recovery probability
</div>

<div class="chain-text">
{best["recovery_probability"] * 100:.1f}%
</div>

</div>

<div class="chain">

<div class="chain-title">
Risk score
</div>

<div class="chain-text">
{best["risk_score"]:.0f}/100
</div>

</div>

<div class="chain">

<div class="chain-title">
Expected recovery
</div>

<div class="chain-text">
₹{best["expected_recoverable_revenue"]:,.0f}
</div>

</div>

</div>
""",
            unsafe_allow_html=True
        )

    with right:

        st.markdown("#### Decision priority")

        st.metric(
            "Priority Score",
            f"{best['priority_score']:,.0f}"
        )

        st.metric(
            "Transaction",
            best["transaction_id"]
        )

        st.metric(
            "Customer",
            best["customer_id"]
        )

        if st.button(
            "▶ Run Recovery Analysis",
            use_container_width=True
        ):

            st.session_state.analysis_runs += 1

            st.success(
                "Recovery analysis refreshed successfully."
            )

            st.rerun()


    # -----------------------------------------------------
    # STATUS MIX
    # -----------------------------------------------------

    st.markdown("### 📡 Recovery Performance")

    if "status" in results.columns:

        status_df = (
            results["status"]
            .value_counts()
            .reset_index()
        )

        status_df.columns = ["Status", "Count"]

        fig = px.pie(
            status_df,
            names="Status",
            values="Count",
            hole=.65
        )

        fig.update_layout(
            paper_bgcolor=CARD,
            plot_bgcolor=CARD,
            font_color=TEXT,
            margin=dict(l=10, r=10, t=20, b=20)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# TRANSACTIONS
# =========================================================

elif page == "Transactions":

    st.header("💳 Transaction Intelligence")

    st.caption(
        "Explore failed and successful payment activity."
    )

    col1, col2, col3 = st.columns(3)

    search = col1.text_input(
        "Search transaction / customer",
        placeholder="TXN_1001"
    )

    status_filter = col2.multiselect(
        "Status",
        sorted(results["status"].astype(str).unique()),
        default=sorted(results["status"].astype(str).unique())
    )

    min_amount = col3.number_input(
        "Minimum amount",
        min_value=0,
        value=0
    )

    view = results.copy()

    if search:

        mask = (
            view["transaction_id"]
            .astype(str)
            .str.contains(search, case=False)
            |
            view["customer_id"]
            .astype(str)
            .str.contains(search, case=False)
        )

        view = view[mask]

    view = view[
        view["status"].astype(str).isin(status_filter)
    ]

    view = view[
        view["amount"] >= min_amount
    ]

    st.write(
        f"**{len(view):,} transactions** match your filters."
    )

    display_columns = [
        "transaction_id",
        "customer_id",
        "amount",
        "risk_score",
        "recovery_probability",
        "expected_recoverable_revenue",
        "recovered_revenue",
        "status"
    ]

    display_columns = [
        x for x in display_columns
        if x in view.columns
    ]

    st.dataframe(
        view[display_columns],
        use_container_width=True,
        height=500
    )

    csv = view.to_csv(index=False)

    st.download_button(
        "📥 Export Transactions CSV",
        csv,
        "recoverx_transactions.csv",
        "text/csv"
    )


# =========================================================
# RECOVERY QUEUE
# =========================================================

elif page == "Recovery Queue":

    st.header("🎯 Smart Recovery Queue")

    st.caption(
        "Prioritized using expected recovery, probability and risk."
    )

    threshold = st.slider(
        "Minimum expected recovery",
        0,
        50000,
        1000,
        step=500
    )

    queue = ranked[
        ranked["expected_recoverable_revenue"] >= threshold
    ].copy()

    st.info(
        f"{len(queue):,} recovery opportunities identified."
    )

    st.dataframe(
        queue[
            [
                "transaction_id",
                "customer_id",
                "amount",
                "risk_score",
                "recovery_probability",
                "expected_recoverable_revenue",
                "priority_score",
                "status"
            ]
        ],
        use_container_width=True,
        height=500
    )

    csv = queue.to_csv(index=False)

    st.download_button(
        "📥 Export Recovery Queue",
        csv,
        "recoverx_priority_queue.csv",
        "text/csv"
    )


# =========================================================
# AGENT DECISIONS
# =========================================================

elif page == "Agent Decisions":

    st.header("🧠 AI Agent Decision Chain")

    transaction_id = st.selectbox(
        "Select recovery case",
        results["transaction_id"].astype(str).tolist()
    )

    case = results[
        results["transaction_id"].astype(str)
        == transaction_id
    ].iloc[0]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Amount",
        f"₹{case['amount']:,.0f}"
    )

    c2.metric(
        "Risk",
        f"{case['risk_score']:.0f}/100"
    )

    c3.metric(
        "Probability",
        f"{case['recovery_probability']*100:.1f}%"
    )

    c4.metric(
        "Expected Recovery",
        f"₹{case['expected_recoverable_revenue']:,.0f}"
    )

    st.markdown("---")

    left, right = st.columns([1.2, 1])

    with left:

        st.subheader("Decision Chain")

        cause = case.get(
            "root_cause.cause",
            "Unknown failure"
        )

        confidence = float(
            case.get(
                "root_cause.confidence",
                0
            )
        )

        explanation = case.get(
            "root_cause.explanation",
            "No explanation available."
        )

        action = case.get(
            "strategy.action",
            "REVIEW"
        )

        reason = case.get(
            "strategy.reason",
            "No reason available."
        )

        policy = case.get(
            "policy.decision",
            "REVIEW"
        )

        policy_reason = case.get(
            "policy.reason",
            "No policy explanation."
        )

        st.markdown(
            f"""
<div class="section-card">

<div class="chain">

<div class="chain-title">
1. 🔍 Diagnose
</div>

<div class="chain-text">
<strong>{cause}</strong><br>
Confidence: {confidence*100:.1f}%<br>
{explanation}
</div>

</div>

<div class="chain">

<div class="chain-title">
2. 🎯 Score
</div>

<div class="chain-text">
Recovery probability:
{case['recovery_probability']*100:.1f}%<br>
Risk score: {case['risk_score']:.0f}/100
</div>

</div>

<div class="chain">

<div class="chain-title">
3. 🤖 Recommend
</div>

<div class="chain-text">
<strong>{action}</strong><br>
{reason}
</div>

</div>

<div class="chain">

<div class="chain-title">
4. 🛡️ Policy
</div>

<div class="chain-text">
<strong>{policy}</strong><br>
{policy_reason}
</div>

</div>

</div>
""",
            unsafe_allow_html=True
        )

    with right:

        st.subheader("Decision Visualization")

        probability = case["recovery_probability"] * 100

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=probability,
                title={"text": "Recovery Probability"},
                gauge={
                    "axis": {
                        "range": [0, 100]
                    },
                    "bar": {
                        "color": CYAN
                    },
                    "steps": [
                        {
                            "range": [0, 40],
                            "color": CORAL
                        },
                        {
                            "range": [40, 70],
                            "color": AMBER
                        },
                        {
                            "range": [70, 100],
                            "color": GREEN
                        }
                    ]
                }
            )
        )

        fig.update_layout(
            paper_bgcolor=CARD,
            font_color=TEXT
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown("---")

    st.subheader("▶ Recovery Execution")

    already_executed = (
        transaction_id
        in st.session_state.executed_cases
    )

    if already_executed:

        st.success(
            "✓ Recovery execution recorded for this case."
        )

    else:

        if st.button(
            "▶ Execute Recovery",
            type="primary",
            use_container_width=True
        ):

            st.session_state.executed_cases.add(
                transaction_id
            )

            event = {
                "timestamp": datetime.now().isoformat(),
                "transaction_id": transaction_id,
                "event": "RECOVERY_EXECUTED",
                "policy": policy,
                "action": action,
                "recovery_probability": float(
                    case["recovery_probability"]
                )
            }

            st.session_state.audit_events.append(event)

            st.success(
                "Recovery action executed in simulation mode."
            )

            st.rerun()


# =========================================================
# POLICY CENTER
# =========================================================

elif page == "Policy Center":

    st.header("🛡️ Policy Center")

    st.caption(
        "Govern what the AI agent is allowed to execute."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Recovery Controls")

        max_auto_amount = st.number_input(
            "Maximum automatic recovery amount",
            min_value=0,
            value=50000,
            step=5000
        )

        min_probability = st.slider(
            "Minimum recovery probability for auto approval",
            0.0,
            1.0,
            0.65
        )

        max_risk = st.slider(
            "Maximum risk score for auto approval",
            0,
            100,
            70
        )

        max_attempts = st.slider(
            "Maximum retry attempts",
            1,
            5,
            3
        )

    with col2:

        st.subheader("Live Policy Simulator")

        amount = st.number_input(
            "Test transaction amount",
            min_value=0,
            value=int(best["amount"])
        )

        probability = st.slider(
            "Test recovery probability",
            0.0,
            1.0,
            float(best["recovery_probability"])
        )

        risk = st.slider(
            "Test risk score",
            0,
            100,
            int(best["risk_score"])
        )

        if amount <= max_auto_amount and \
           probability >= min_probability and \
           risk <= max_risk:

            st.success(
                "✓ ALLOW — automatic recovery permitted"
            )

        elif probability >= 0.40:

            st.warning(
                "⚠ HUMAN APPROVAL — review required"
            )

        else:

            st.error(
                "✕ BLOCK — recovery not recommended"
            )

    st.markdown("---")

    st.subheader("Policy Rules")

    policy_df = pd.DataFrame({
        "Rule": [
            "Maximum auto-recovery amount",
            "Minimum recovery probability",
            "Maximum risk score",
            "Maximum retry attempts"
        ],
        "Current Value": [
            f"₹{max_auto_amount:,.0f}",
            f"{min_probability*100:.0f}%",
            f"{max_risk}/100",
            max_attempts
        ],
        "Purpose": [
            "Limit financial exposure",
            "Avoid low-confidence actions",
            "Protect risky transactions",
            "Prevent repeated customer friction"
        ]
    })

    st.dataframe(
        policy_df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# AUDIT TRAIL
# =========================================================

elif page == "Audit Trail":

    st.header("📜 Audit Trail")

    st.caption(
        "Every simulated recovery decision is traceable."
    )

    events = []

    # Existing JSONL audit log
    possible_logs = [
        "audit_log.jsonl",
        "data/audit_log.jsonl"
    ]

    for log_path in possible_logs:

        if os.path.exists(log_path):

            try:

                with open(
                    log_path,
                    "r",
                    encoding="utf-8"
                ) as f:

                    for line in f:

                        if line.strip():

                            try:
                                events.append(
                                    json.loads(line)
                                )
                            except:
                                pass

            except:
                pass

    events.extend(
        st.session_state.audit_events
    )

    if not events:

        st.info(
            "No audit events available yet. "
            "Execute a recovery from Agent Decisions."
        )

    else:

        audit_df = pd.DataFrame(events)

        search = st.text_input(
            "🔎 Search audit trail",
            placeholder="transaction ID or event"
        )

        if search:

            mask = audit_df.astype(str).apply(
                lambda row:
                row.str.contains(
                    search,
                    case=False
                ).any(),
                axis=1
            )

            audit_df = audit_df[mask]

        st.success(
            f"{len(audit_df):,} audit events"
        )

        st.dataframe(
            audit_df,
            use_container_width=True,
            height=500
        )

        st.download_button(
            "📥 Export Audit Trail",
            audit_df.to_csv(index=False),
            "recoverx_audit_trail.csv",
            "text/csv"
        )


# =========================================================
# RECOVERY ASSISTANT
# =========================================================

elif page == "Recovery Assistant":

    st.header("🤖 Ask the Recovery Desk")

    st.caption(
        "Answers are grounded in the current RecoverX workspace."
    )

    st.markdown(
        f"""
<div class="ai-card">

<div class="eyebrow">
RECOVERY INTELLIGENCE DESK
</div>

<h2>
What should we inspect?
</h2>

<p style="color:{MUTED};">
Ask about revenue risk, failed payments,
priority cases, recovery performance or strategies.
</p>

</div>
""",
        unsafe_allow_html=True
    )

    question = st.text_input(
        "Ask RecoverX",
        placeholder="What is driving revenue at risk?"
    )

    if st.button(
        "Ask RecoverX",
        type="primary"
    ):

        q = question.lower()

        if "risk" in q:

            st.success(
                f"₹{revenue_at_risk:,.0f} is currently "
                f"at risk across {failed_count:,} failed transactions. "
                f"The estimated recoverable pool is "
                f"₹{expected_recoverable:,.0f}."
            )

        elif "recover" in q and "rate" in q:

            st.success(
                f"The current recovery rate is "
                f"{recovery_rate:.1f}%. "
                f"₹{recovered:,.0f} has been recovered "
                f"against ₹{revenue_at_risk:,.0f} at risk."
            )

        elif "first" in q or "priority" in q:

            st.success(
                f"The highest-priority case is "
                f"{best['transaction_id']} for customer "
                f"{best['customer_id']}. "
                f"It has an expected recovery of "
                f"₹{best['expected_recoverable_revenue']:,.0f}."
            )

        elif "strategy" in q:

            strategy_df = (
                results.groupby(
                    "strategy.action"
                )["recovered_revenue"]
                .sum()
                .sort_values(
                    ascending=False
                )
            )

            if len(strategy_df):

                top_strategy = strategy_df.index[0]

                st.success(
                    f"The strongest recovery strategy by "
                    f"recovered revenue is "
                    f"'{top_strategy}', generating "
                    f"₹{strategy_df.iloc[0]:,.0f}."
                )

        elif "failure" in q:

            if "failure_reason" in failed.columns:

                failure = (
                    failed.groupby(
                        "failure_reason"
                    )["amount"]
                    .sum()
                    .sort_values(
                        ascending=False
                    )
                )

                top_failure = failure.index[0]

                st.success(
                    f"The largest revenue exposure comes from "
                    f"'{top_failure}', representing "
                    f"₹{failure.iloc[0]:,.0f}."
                )

        else:

            st.info(
                "Try asking: "
                "'What is driving revenue at risk?', "
                "'Which cases should I review first?', "
                "'Explain the recovery rate', or "
                "'Which strategy performs best?'"
            )

    st.markdown("---")

    st.subheader("Suggested Questions")

    q1, q2, q3 = st.columns(3)

    if q1.button("What is driving revenue at risk?"):
        st.success(
            f"Revenue at risk: ₹{revenue_at_risk:,.0f}"
        )

    if q2.button("Which cases should I review first?"):
        st.success(
            f"Top case: {best['transaction_id']}"
        )

    if q3.button("Explain the recovery rate"):
        st.success(
            f"Recovery rate: {recovery_rate:.1f}%"
        )


# =========================================================
# ANALYTICS
# =========================================================

elif page == "Analytics":

    st.header("📊 Recovery Analytics")

    col1, col2 = st.columns(2)

    with col1:

        if "failure_reason" in failed.columns:

            failure_df = (
                failed.groupby(
                    "failure_reason"
                )["amount"]
                .sum()
                .reset_index()
                .sort_values(
                    "amount",
                    ascending=False
                )
            )

            fig = px.bar(
                failure_df,
                x="failure_reason",
                y="amount",
                title="Revenue At Risk by Failure"
            )

            fig.update_layout(
                paper_bgcolor=CARD,
                plot_bgcolor=CARD,
                font_color=TEXT
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    with col2:

        strategy_df = (
            results.groupby(
                "strategy.action"
            )["recovered_revenue"]
            .sum()
            .reset_index()
            .sort_values(
                "recovered_revenue",
                ascending=False
            )
        )

        fig = px.bar(
            strategy_df,
            x="strategy.action",
            y="recovered_revenue",
            title="Recovered Revenue by Strategy"
        )

        fig.update_layout(
            paper_bgcolor=CARD,
            plot_bgcolor=CARD,
            font_color=TEXT
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # -----------------------------------------------------
    # PROBABILITY DISTRIBUTION
    # -----------------------------------------------------

    st.subheader("🎯 Recovery Probability Distribution")

    fig = px.histogram(
        results,
        x="recovery_probability",
        nbins=20,
        title="Distribution of Recovery Probability"
    )

    fig.update_layout(
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font_color=TEXT
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # -----------------------------------------------------
    # RISK VS RECOVERY
    # -----------------------------------------------------

    st.subheader("⚖️ Risk vs Recovery Opportunity")

    fig = px.scatter(
        results,
        x="risk_score",
        y="expected_recoverable_revenue",
        size="amount",
        hover_name="transaction_id",
        color="recovery_probability",
        title="Risk Score vs Expected Recovery"
    )

    fig.update_layout(
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font_color=TEXT
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # -----------------------------------------------------
    # PERFORMANCE TABLE
    # -----------------------------------------------------

    st.subheader("📈 Recovery Statistics")

    stats = pd.DataFrame({
        "Metric": [
            "Total transactions",
            "Failed transactions",
            "Revenue at risk",
            "Expected recoverable",
            "Revenue recovered",
            "Recovery rate",
            "Recovery candidates",
            "Successful recoveries"
        ],
        "Value": [
            len(transactions),
            failed_count,
            f"₹{revenue_at_risk:,.0f}",
            f"₹{expected_recoverable:,.0f}",
            f"₹{recovered:,.0f}",
            f"{recovery_rate:.1f}%",
            candidate_count,
            recovered_cases
        ]
    })

    st.dataframe(
        stats,
        use_container_width=True,
        hide_index=True
    )
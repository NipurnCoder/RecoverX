# RecoverX — AI-Powered Revenue Recovery System

> **Turn failed payments into measurable recovery opportunities.**

RecoverX is an AI-powered revenue recovery system designed to identify failed payments, estimate recovery potential, determine the root cause, recommend the next best recovery action, enforce safety policies, and measure recovered revenue.

The system combines **risk scoring, AI-agent decision logic, deterministic policy enforcement, payment simulation, human approval, prioritization, and audit logging** into a single end-to-end workflow.

---

## 🚀 Project Overview

Payment failures do not always mean permanent revenue loss.

Transactions can fail because of:

* Bank timeouts
* Network errors
* Insufficient funds
* Expired payment methods
* Payment limits
* Authentication failures
* Suspected fraud

Different failure reasons require different recovery strategies.

RecoverX analyzes each failed transaction and determines:

1. **How likely is this payment to be recovered?**
2. **How much revenue is potentially recoverable?**
3. **Why did the payment fail?**
4. **What recovery action should be attempted?**
5. **Is the action allowed by the safety policies?**
6. **Does the recovery require human approval?**
7. **How much revenue was actually recovered?**

---

# 🎯 Key Features

### 🔍 1. Revenue Risk Detection

Identifies failed transactions and calculates the amount of revenue currently at risk.

### 📊 2. Recovery Probability

Estimates the probability that a failed transaction can be successfully recovered using:

* Failure reason
* Customer payment history
* Payment success rate
* Engagement score
* Previous attempts

### 💰 3. Expected Recoverable Revenue

Calculates the expected monetary recovery opportunity:

```text
Expected Recoverable Revenue
= Transaction Amount × Recovery Probability
```

### 🧠 4. Root Cause Analysis

Classifies payment failures into meaningful causes such as:

```text
BANK_TIMEOUT
        ↓
TEMPORARY_BANK_FAILURE
```

```text
CARD_EXPIRED
        ↓
EXPIRED_PAYMENT_METHOD
```

```text
FRAUD_SUSPECTED
        ↓
POTENTIAL_FRAUD
```

### 🤖 5. Recovery Strategy Agent

Selects an appropriate recovery strategy based on the failure reason and recovery probability.

Supported strategies include:

* Delayed Retry
* Payment Link
* Reminder
* Payment Method Update
* Human Escalation

### 🛡️ 6. Policy Engine

The AI recommendation must pass through deterministic safety rules before execution.

Policies include:

* Maximum retry limits
* Maximum customer contact limits
* Fraud protection
* High-value transaction approval
* Controlled execution

### 👤 7. Human-in-the-Loop Approval

High-value transactions are not automatically executed.

Instead:

```text
High-Value Transaction
        ↓
Human Approval Request
        ↓
PENDING
        ↓
APPROVE / REJECT
        ↓
Recovery Execution
```

### 💳 8. Payment Simulator

RecoverX currently uses a payment simulator to safely demonstrate recovery execution without moving real customer money.

This makes the project suitable for testing and demonstrations.

### ⭐ 9. Next Best Recovery

Recovery opportunities are ranked using:

* Expected recoverable revenue
* Risk score
* Customer friction

This allows the system to identify the most valuable recovery opportunity first.

### 📝 10. Audit Logging

Important system decisions and outcomes are recorded in an audit log.

The audit trail includes:

* Timestamp
* Transaction ID
* Recovery strategy
* Recovery probability
* Expected revenue
* Risk score
* Policy decision
* Human approval request
* Recovery result

---

# 🏗️ System Architecture

```text
                 ┌──────────────────────┐
                 │   Transaction Data   │
                 │   Customer Data      │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │     Risk Engine      │
                 │ Recovery Probability │
                 │ Expected Revenue      │
                 │ Risk Score            │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Root Cause Agent   │
                 │ Failure Classification│
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Recovery Strategy    │
                 │       Agent          │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    Policy Engine     │
                 │  Safety & Guardrails │
                 └──────────┬───────────┘
                            │
                  ┌─────────┴─────────┐
                  │                   │
                  ▼                   ▼
           ┌──────────────┐    ┌───────────────┐
           │ Auto Recovery│    │Human Approval │
           └──────┬───────┘    └───────┬───────┘
                  │                    │
                  └─────────┬──────────┘
                            ▼
                 ┌──────────────────────┐
                 │  Payment Simulator   │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Recovery Outcome     │
                 │ Recovered / Failed   │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │     Audit Logger     │
                 └──────────────────────┘
```

---

# 📁 Project Structure

```text
RecoverX/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── risk_engine.py
│   ├── agents.py
│   ├── policy_engine.py
│   ├── recovery_engine.py
│   ├── simulator.py
│   ├── friction.py
│   ├── prioritization.py
│   ├── audit.py
│   └── approval.py
│
├── data/
│   ├── transactions.csv
│   ├── customers.csv
│   └── audit_log.jsonl
│
├── frontend/
│   └── app.py
│
├── generate_data.py
├── run_demo.py
├── test_approval.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🔄 End-to-End Workflow

RecoverX follows the workflow:

```text
Detect
  ↓
Predict
  ↓
Diagnose
  ↓
Recommend
  ↓
Validate
  ↓
Human Approval (if required)
  ↓
Execute
  ↓
Measure
  ↓
Audit
```

---

# 📊 Recovery Scoring

## Recovery Probability

The system starts with a base probability and adjusts it based on transaction and customer characteristics.

Factors include:

* Failure reason
* Customer success rate
* Engagement score
* Previous attempts

The probability is bounded between:

```text
0.02 and 0.98
```

---

## Risk Score

RecoverX combines recovery probability and transaction value to calculate a risk score.

The score helps prioritize valuable recovery opportunities.

---

## Priority Score

Recovery opportunities are ranked using:

```text
Priority Score
=
(Expected Recoverable Revenue × Risk Score)
÷ Customer Friction
```

This helps the system balance:

**Revenue Opportunity + Recovery Probability + Customer Experience**

---

# 🛡️ Safety & Guardrails

RecoverX follows a bounded automation approach.

### Fraud Protection

```text
FRAUD_SUSPECTED
       ↓
NO AUTOMATIC RETRY
```

### Retry Limit

The system prevents unlimited retry attempts.

### Customer Contact Limit

The system limits repeated customer messages.

### High-Value Transactions

Transactions above the configured threshold require human approval.

```text
Amount > ₹50,000
        ↓
HUMAN_APPROVAL
```

This ensures that the AI system does not have unrestricted execution authority.

---

# 👤 Human Approval Workflow

For high-value transactions:

```text
Transaction
     ↓
Policy Engine
     ↓
HUMAN_APPROVAL
     ↓
Approval Request Created
     ↓
PENDING
     ↓
 ┌───────────────┐
 │               │
 ▼               ▼
APPROVE        REJECT
 │               │
 ▼               ▼
Execute         Stop
 │
 ▼
Recovery Result
```

---

# 📝 Audit Trail

RecoverX maintains an audit trail using JSON Lines.

Example events include:

```text
RECOVERY_DECISION
HUMAN_APPROVAL_REQUESTED
RECOVERY_RESULT
APPROVED_RECOVERY_RESULT
```

This provides traceability for recovery decisions and outcomes.

---

# 🖥️ Dashboard

The Streamlit dashboard provides an operational view of the recovery system.

The dashboard includes:

### Key Metrics

* Revenue at Risk
* Expected Recoverable Revenue
* Recovery Rate
* Transaction Count

### Recovery Opportunities

Provides transaction-level information including:

* Transaction ID
* Customer
* Amount
* Failure Reason
* Recovery Probability
* Expected Recoverable Revenue
* Risk Score
* Friction
* Recommended Strategy

### Next Best Recovery

Highlights the highest-priority recovery opportunity.

The operator can immediately see:

* Customer
* Revenue at Risk
* Expected Recovery
* Priority Score
* Recovery Probability
* Friction
* Risk Score
* Recommended Action

---

# 🧪 Safe Demonstration

RecoverX currently uses simulated payment execution.

No real customer money is moved.

This allows the complete recovery workflow to be demonstrated safely:

```text
Failed Payment
      ↓
AI Analysis
      ↓
Recovery Recommendation
      ↓
Policy Validation
      ↓
Simulated Recovery
      ↓
Recovered Revenue
```

---

# ⚙️ Technology Stack

| Technology   | Purpose                 |
| ------------ | ----------------------- |
| Python       | Core application logic  |
| FastAPI      | Backend REST API        |
| Streamlit    | Interactive dashboard   |
| Pandas       | Data processing         |
| NumPy        | Numerical computation   |
| Scikit-learn | Data/ML utilities       |
| Pydantic     | Data validation         |
| Plotly       | Dashboard visualization |
| JSONL        | Audit logging           |

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd RecoverX
```

## 2. Create a virtual environment

### Windows

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

## 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

# 📦 Generate Dataset

If the dataset is not already available:

```powershell
python generate_data.py
```

This generates:

```text
data/transactions.csv
data/customers.csv
```

---

# ▶️ Run the Backend

Start the FastAPI server:

```powershell
python -m uvicorn backend.main:app --reload
```

The API will be available locally at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🖥️ Run the Dashboard

Open another terminal with the virtual environment activated.

Run:

```powershell
streamlit run frontend/app.py
```

The dashboard will open at:

```text
http://localhost:8501
```

---

# 🧪 Test Recovery

The recovery API can be tested using:

```text
POST /recover/{transaction_id}
```

For example:

```text
POST /recover/TXN001
```

The system will:

1. Load the transaction
2. Find the customer
3. Calculate recovery probability
4. Calculate expected recoverable revenue
5. Identify the root cause
6. Select a recovery strategy
7. Evaluate policy
8. Execute allowed recovery
9. Record the result
10. Write an audit event

---

# 👤 Test Human Approval

The project includes a controlled high-value test.

Run:

```powershell
python test_approval.py
```

This creates a temporary high-value transaction in memory.

It does **not modify the original transaction dataset**.

The transaction is passed through the policy engine and generates:

```text
HUMAN_APPROVAL
```

with:

```text
PENDING
```

approval status.

---

# 🔌 API Endpoints

| Method | Endpoint                    | Purpose                |
| ------ | --------------------------- | ---------------------- |
| GET    | `/`                         | API information        |
| GET    | `/health`                   | Health check           |
| POST   | `/recover/{transaction_id}` | Start recovery         |
| GET    | `/approvals/pending`        | View pending approvals |
| POST   | `/approve/{transaction_id}` | Approve recovery       |
| POST   | `/reject/{transaction_id}`  | Reject recovery        |

---

# 🔐 Design Principles

RecoverX follows several important design principles:

### 1. AI recommends, policy decides

The AI-style agents recommend recovery actions, but the Policy Engine determines whether the action is permitted.

### 2. Bounded automation

The system has limits on retries and customer communication.

### 3. Human-in-the-loop

High-value recovery actions require human approval.

### 4. Fraud-aware recovery

Suspected fraud is not automatically retried.

### 5. Measurable outcomes

The system measures actual recovered revenue rather than only generating recommendations.

### 6. Full auditability

Important decisions and outcomes are recorded in the audit log.

---

# 🎯 Business Value

RecoverX can help businesses:

* Reduce revenue leakage
* Prioritize valuable failed payments
* Automate low-risk recovery actions
* Reduce unnecessary customer friction
* Prevent unsafe automated retries
* Improve recovery operations
* Measure actual recovered revenue
* Maintain an auditable recovery process

---

# 🔮 Future Improvements

The current project uses a payment simulator for safe demonstration.

Future versions could integrate:

* Razorpay Test Mode
* Real payment webhooks
* Production payment events
* Real-time recovery monitoring
* More advanced ML models
* LLM-based root-cause reasoning
* A/B testing of recovery strategies
* Recovery campaign optimization
* Merchant-specific policies
* Real-time revenue recovery analytics

The architecture is designed so that the simulator can eventually be replaced with a controlled payment-gateway integration.

---

# 📌 Project Objective

The objective of RecoverX is not simply to predict failed payments.

It is to build a complete recovery decision system that can:

```text
Find revenue at risk
        ↓
Understand why it is at risk
        ↓
Estimate recovery potential
        ↓
Choose the best intervention
        ↓
Apply safety policies
        ↓
Execute safely
        ↓
Measure recovered revenue
        ↓
Create an audit trail
```

---

# 🏆 Key Takeaway

> **RecoverX doesn't just ask, "What went wrong?"**
>
> **It asks, "What can we recover, what is the safest way to recover it, and how much revenue did we actually win back?"**

---

## 👨‍💻 Author

**NIPURN**

AI / Machine Learning Project — Revenue Recovery

---

## 📄 License

This project is developed for educational and internship demonstration purposes.

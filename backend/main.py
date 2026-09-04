from fastapi import FastAPI

from backend.recovery_engine import RecoveryEngine

from backend.approval import ApprovalManager

import pandas as pd


app = FastAPI(
    title="RecoverX API",
    description="AI Revenue Recovery Agent",
    version="1.0"
)

approval_manager = ApprovalManager()

engine = RecoveryEngine(
    approval_manager=approval_manager
)


@app.get("/")
def home():

    return {
        "name": "RecoverX",
        "status": "running",
        "description":
            "AI Revenue Recovery Agent"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/recover/{transaction_id}")
def recover(transaction_id: str):

    transactions = pd.read_csv(
        "data/transactions.csv"
    )

    customers = pd.read_csv(
        "data/customers.csv"
    )

    transaction_rows = transactions[
        transactions["transaction_id"]
        == transaction_id
    ]

    if transaction_rows.empty:

        return {
            "error": "Transaction not found"
        }

    transaction = (
        transaction_rows.iloc[0].to_dict()
    )

    customer = customers[
        customers["customer_id"]
        == transaction["customer_id"]
    ].iloc[0].to_dict()

    result = engine.process(
        transaction,
        customer
    )

    return result

@app.get("/approvals/pending")
def get_pending_approvals():

    return {
        "count": len(
            approval_manager.get_pending_requests()
        ),
        "requests":
            approval_manager.get_pending_requests()
    } 


@app.post("/approve/{transaction_id}")
def approve_recovery(transaction_id: str):

    # Step 1: Approve the request
    approval_result = approval_manager.approve(
        transaction_id
    )

    if not approval_result["success"]:
        return approval_result

    # Step 2: Get approved request
    request = approval_result["request"]

    # Step 3: Load transaction data
    transactions = pd.read_csv(
        "data/transactions.csv"
    )

    transaction_rows = transactions[
        transactions["transaction_id"]
        == transaction_id
    ]

    if transaction_rows.empty:

        return {
            "success": False,
            "message": "Transaction not found."
        }

    transaction = (
        transaction_rows.iloc[0].to_dict()
    )

    # Step 4: Execute approved recovery
    transaction["strategy"] = request["strategy"]

    execution_result = engine.execute_approved(
        transaction
    )

    # Step 5: Return complete result
    return {
        "success": True,
        "approval": approval_result,
        "recovery": execution_result
    }  

@app.post("/reject/{transaction_id}")
def reject_recovery(transaction_id: str):

    result = approval_manager.reject(
        transaction_id
    )

    return result    
   
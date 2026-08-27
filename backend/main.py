from fastapi import FastAPI

from backend.recovery_engine import RecoveryEngine

import pandas as pd


app = FastAPI(
    title="RecoverX API",
    description="AI Revenue Recovery Agent",
    version="1.0"
)

engine = RecoveryEngine()


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
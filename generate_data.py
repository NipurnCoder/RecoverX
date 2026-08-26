import pandas as pd
import numpy as np
import random
import os

random.seed(42)
np.random.seed(42)

os.makedirs("data", exist_ok=True)

NUM_CUSTOMERS = 5000
NUM_TRANSACTIONS = 20000

failure_reasons = [
    "BANK_TIMEOUT",
    "NETWORK_ERROR",
    "INSUFFICIENT_FUNDS",
    "CARD_EXPIRED",
    "LIMIT_EXCEEDED",
    "AUTHENTICATION_FAILED",
    "FRAUD_SUSPECTED"
]

payment_methods = [
    "CARD",
    "UPI",
    "NETBANKING",
    "WALLET"
]

customers = []

for i in range(NUM_CUSTOMERS):

    successful = np.random.randint(1, 40)
    failed = np.random.randint(0, 8)

    customers.append({
        "customer_id": f"CUST_{i+1:05d}",
        "account_age_days": np.random.randint(30, 1500),
        "successful_payments": successful,
        "failed_payments": failed,
        "average_transaction": round(np.random.uniform(300, 25000), 2),
        "lifetime_value": round(np.random.uniform(1000, 500000), 2),
        "engagement_score": round(np.random.uniform(0.1, 1.0), 2)
    })

customers_df = pd.DataFrame(customers)

transactions = []

for i in range(NUM_TRANSACTIONS):

    customer = random.choice(customers)

    status = np.random.choice(
        ["SUCCESS", "FAILED"],
        p=[0.72, 0.28]
    )

    amount = round(
        max(
            100,
            np.random.normal(
                customer["average_transaction"],
                customer["average_transaction"] * 0.35
            )
        ),
        2
    )

    if status == "FAILED":

        reason = np.random.choice(
            failure_reasons,
            p=[
                0.22,
                0.18,
                0.20,
                0.12,
                0.10,
                0.10,
                0.08
            ]
        )

    else:
        reason = None

    transactions.append({
        "transaction_id": f"TXN_{i+1:06d}",
        "customer_id": customer["customer_id"],
        "amount": amount,
        "payment_method": random.choice(payment_methods),
        "status": status,
        "failure_reason": reason,
        "attempt_number": np.random.randint(1, 3),
        "days_since_last_payment": np.random.randint(0, 60)
    })

transactions_df = pd.DataFrame(transactions)

transactions_df.to_csv(
    "data/transactions.csv",
    index=False
)

customers_df.to_csv(
    "data/customers.csv",
    index=False
)

print("Dataset generated successfully.")

print(f"Customers: {len(customers_df)}")
print(f"Transactions: {len(transactions_df)}")

failed = transactions_df[
    transactions_df["status"] == "FAILED"
]

print(f"Failed payments: {len(failed)}")
print(
    f"Revenue at risk: ₹{failed['amount'].sum():,.2f}"
)
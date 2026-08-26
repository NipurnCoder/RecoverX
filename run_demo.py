import pandas as pd

from backend.recovery_engine import RecoveryEngine


transactions = pd.read_csv(
    "data/transactions.csv"
)

customers = pd.read_csv(
    "data/customers.csv"
)

failed = transactions[
    transactions["status"] == "FAILED"
].copy()

engine = RecoveryEngine()

results = []

for _, transaction in failed.iterrows():

    customer = customers[
        customers["customer_id"]
        == transaction["customer_id"]
    ].iloc[0]

    result = engine.process(
        transaction.to_dict(),
        customer.to_dict()
    )

    results.append(result)


results_df = pd.json_normalize(
    results
)

results_df.to_csv(
    "data/recovery_results.csv",
    index=False
)

print("\n================================")
print("       RECOVERX RESULTS")
print("================================")

total_at_risk = (
    failed["amount"].sum()
)

total_expected = (
    results_df[
        "expected_recoverable_revenue"
    ].sum()
)

total_recovered = (
    results_df[
        "recovered_revenue"
    ].sum()
)

recovery_rate = (
    total_recovered / total_at_risk * 100
)

print(
    f"Revenue At Risk: ₹{total_at_risk:,.2f}"
)

print(
    f"Expected Recoverable: ₹{total_expected:,.2f}"
)

print(
    f"Revenue Recovered: ₹{total_recovered:,.2f}"
)

print(
    f"Recovery Rate: {recovery_rate:.2f}%"
)

print("\nStatus:")
print(
    results_df["status"].value_counts()
)
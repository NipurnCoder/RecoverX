# def calculate_priority(
#     expected_revenue,
#     friction,
#     risk_score
# ):

#     friction = max(friction, 1)

#     return round(
#         (
#             expected_revenue
#             * (risk_score / 100)
#         ) / friction,
#         2
#     )


# def rank_recovery_opportunities(
#     results
# ):

#     results = results.copy()

#     results["priority_score"] = (
#         results.apply(
#             lambda row:
#             calculate_priority(
#                 row[
#                     "expected_recoverable_revenue"
#                 ],
#                 row["friction"],
#                 row["risk_score"]
#             ),
#             axis=1
#         )
#     )

#     return results.sort_values(
#         "priority_score",
#         ascending=False
#     )

def calculate_priority(
    expected_revenue,
    friction,
    risk_score
):

    friction = max(friction, 1)

    priority = (
        expected_revenue
        * (risk_score / 100)
    ) / friction

    return round(priority, 2)


def rank_recovery_opportunities(results):

    results = results.copy()

    results["priority_score"] = results.apply(
        lambda row:
        calculate_priority(
            row["expected_recoverable_revenue"],
            row["friction"],
            row["risk_score"]
        ),
        axis=1
    )

    return results.sort_values(
        "priority_score",
        ascending=False
    )
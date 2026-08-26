def calculate_recovery_probability(transaction, customer):

    score = 0.50

    reason = transaction["failure_reason"]

    # Temporary failures are highly recoverable
    if reason == "BANK_TIMEOUT":
        score += 0.25

    elif reason == "NETWORK_ERROR":
        score += 0.22

    elif reason == "INSUFFICIENT_FUNDS":
        score += 0.05

    elif reason == "CARD_EXPIRED":
        score += 0.08

    elif reason == "LIMIT_EXCEEDED":
        score -= 0.05

    elif reason == "AUTHENTICATION_FAILED":
        score -= 0.10

    elif reason == "FRAUD_SUSPECTED":
        score -= 0.45

    # Customer history
    successful = customer["successful_payments"]
    failed = customer["failed_payments"]

    total = successful + failed

    if total > 0:

        success_rate = successful / total

        if success_rate > 0.80:
            score += 0.15

        elif success_rate < 0.40:
            score -= 0.15

    # Engagement
    score += (
        customer["engagement_score"] - 0.5
    ) * 0.20

    # Retry penalty
    if transaction["attempt_number"] >= 2:
        score -= 0.15

    score = max(0.02, min(score, 0.98))

    return round(score, 4)


def calculate_expected_recoverable_revenue(
    amount,
    recovery_probability
):

    return round(
        amount * recovery_probability,
        2
    )


def calculate_risk_score(
    amount,
    recovery_probability
):

    # Higher amount + higher probability
    # = higher priority

    raw_score = (
        recovery_probability * 70
        + min(amount / 100000, 1) * 30
    )

    return round(
        min(raw_score, 100),
        2
    )
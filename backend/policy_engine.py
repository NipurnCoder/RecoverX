MAX_RETRIES = 2
MAX_MESSAGES = 2

HUMAN_APPROVAL_LIMIT = 50000


class PolicyEngine:

    def evaluate(
        self,
        transaction,
        recommended_action,
        retry_count=0,
        message_count=0
    ):

        amount = transaction["amount"]

        reason = transaction["failure_reason"]

        # Fraud = never automatically recover
        if reason == "FRAUD_SUSPECTED":

            return {
                "decision": "DENY",
                "reason": "Fraud-related payment cannot be auto-retried."
            }

        # Retry limit
        if (
            recommended_action == "DELAYED_RETRY"
            and retry_count >= MAX_RETRIES
        ):

            return {
                "decision": "STOP",
                "reason": "Maximum retry limit reached."
            }

        # Message limit
        if (
            recommended_action in [
                "PAYMENT_LINK",
                "REMINDER"
            ]
            and message_count >= MAX_MESSAGES
        ):

            return {
                "decision": "STOP",
                "reason": "Maximum customer contact limit reached."
            }

        # High value transactions
        if amount > HUMAN_APPROVAL_LIMIT:

            return {
                "decision": "HUMAN_APPROVAL",
                "reason":
                    f"Transaction exceeds ₹{HUMAN_APPROVAL_LIMIT:,}."
            }

        return {
            "decision": "ALLOW",
            "reason": "Action satisfies all recovery policies."
        }
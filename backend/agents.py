class RootCauseAgent:

    def analyze(self, transaction):

        reason = transaction["failure_reason"]

        mapping = {

            "BANK_TIMEOUT": {
                "cause": "TEMPORARY_BANK_FAILURE",
                "confidence": 0.94,
                "explanation":
                    "The payment appears to have failed because "
                    "of a temporary bank or gateway timeout."
            },

            "NETWORK_ERROR": {
                "cause": "NETWORK_DEGRADATION",
                "confidence": 0.91,
                "explanation":
                    "The transaction encountered a temporary "
                    "network communication problem."
            },

            "INSUFFICIENT_FUNDS": {
                "cause": "INSUFFICIENT_FUNDS",
                "confidence": 0.97,
                "explanation":
                    "The customer's available balance may not "
                    "be sufficient for the transaction."
            },

            "CARD_EXPIRED": {
                "cause": "EXPIRED_PAYMENT_METHOD",
                "confidence": 0.99,
                "explanation":
                    "The payment method is likely expired."
            },

            "LIMIT_EXCEEDED": {
                "cause": "PAYMENT_LIMIT",
                "confidence": 0.95,
                "explanation":
                    "The payment may have exceeded a bank or "
                    "payment-method limit."
            },

            "AUTHENTICATION_FAILED": {
                "cause": "AUTHENTICATION_FAILURE",
                "confidence": 0.94,
                "explanation":
                    "The customer authentication step failed."
            },

            "FRAUD_SUSPECTED": {
                "cause": "POTENTIAL_FRAUD",
                "confidence": 0.98,
                "explanation":
                    "The transaction has a potential fraud signal "
                    "and should not be automatically retried."
            }
        }

        return mapping.get(
            reason,
            {
                "cause": "UNKNOWN",
                "confidence": 0.50,
                "explanation":
                    "The root cause could not be determined."
            }
        )


class RecoveryStrategyAgent:

    def choose_strategy(
        self,
        transaction,
        root_cause,
        recovery_probability
    ):

        cause = root_cause["cause"]

        if cause == "POTENTIAL_FRAUD":

            return {
                "action": "HUMAN_ESCALATION",
                "reason":
                    "Fraud-related transactions require human review."
            }

        if cause == "EXPIRED_PAYMENT_METHOD":

            return {
                "action": "PAYMENT_METHOD_UPDATE",
                "reason":
                    "The customer should update the expired payment method."
            }

        if cause == "TEMPORARY_BANK_FAILURE":

            return {
                "action": "DELAYED_RETRY",
                "reason":
                    "Temporary bank failures have a high recovery probability."
            }

        if cause == "NETWORK_DEGRADATION":

            return {
                "action": "DELAYED_RETRY",
                "reason":
                    "Network failures are often transient."
            }

        if cause == "INSUFFICIENT_FUNDS":

            if recovery_probability >= 0.60:

                return {
                    "action": "PAYMENT_LINK",
                    "reason":
                        "Customer has a reasonable recovery probability."
                }

            return {
                "action": "REMINDER",
                "reason":
                    "Recovery probability is moderate."
            }

        if cause == "PAYMENT_LIMIT":

            return {
                "action": "PAYMENT_LINK",
                "reason":
                    "Alternative payment method may succeed."
            }

        if cause == "AUTHENTICATION_FAILURE":

            return {
                "action": "PAYMENT_LINK",
                "reason":
                    "A fresh payment attempt may resolve authentication issues."
            }

        return {
            "action": "HUMAN_ESCALATION",
            "reason": "Unknown failure requires review."
        }
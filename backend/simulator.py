import random


class PaymentSimulator:

    def retry_payment(self, transaction):

        reason = transaction["failure_reason"]

        probability = {

            "BANK_TIMEOUT": 0.85,

            "NETWORK_ERROR": 0.82,

            "INSUFFICIENT_FUNDS": 0.55,

            "CARD_EXPIRED": 0.65,

            "LIMIT_EXCEEDED": 0.45,

            "AUTHENTICATION_FAILED": 0.40,

            "FRAUD_SUSPECTED": 0.02
        }.get(reason, 0.40)

        success = random.random() < probability

        return {
            "success": success,
            "amount": transaction["amount"],
            "message":
                "PAYMENT_SUCCESS"
                if success
                else "PAYMENT_FAILED"
        }

    def payment_link(self, transaction):

        probability = 0.60

        success = random.random() < probability

        return {
            "success": success,
            "amount": transaction["amount"],
            "message":
                "PAYMENT_LINK_SUCCESS"
                if success
                else "PAYMENT_LINK_NOT_USED"
        }

    def reminder(self, transaction):

        return {
            "success": False,
            "amount": transaction["amount"],
            "message": "REMINDER_SENT"
        }
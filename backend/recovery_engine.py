from backend.risk_engine import (
    calculate_recovery_probability,
    calculate_expected_recoverable_revenue,
    calculate_risk_score
)

from backend.agents import (
    RootCauseAgent,
    RecoveryStrategyAgent
)

from backend.policy_engine import PolicyEngine

from backend.simulator import PaymentSimulator

from backend.friction import calculate_friction


class RecoveryEngine:

    def __init__(self):

        self.root_agent = RootCauseAgent()

        self.strategy_agent = RecoveryStrategyAgent()

        self.policy_engine = PolicyEngine()

        self.payment_simulator = PaymentSimulator()

    def process(
        self,
        transaction,
        customer
    ):

        # --------------------------------
        # STEP 1: Risk
        # --------------------------------

        recovery_probability = (
            calculate_recovery_probability(
                transaction,
                customer
            )
        )

        expected_revenue = (
            calculate_expected_recoverable_revenue(
                transaction["amount"],
                recovery_probability
            )
        )

        risk_score = calculate_risk_score(
            transaction["amount"],
            recovery_probability
        )

        # --------------------------------
        # STEP 2: Root Cause
        # --------------------------------

        root_cause = self.root_agent.analyze(
            transaction
        )

        # --------------------------------
        # STEP 3: Strategy
        # --------------------------------

        strategy = (
            self.strategy_agent.choose_strategy(
                transaction,
                root_cause,
                recovery_probability
            )
        )

        friction = calculate_friction(
            strategy["action"]
        )

        # --------------------------------
        # STEP 4: Policy
        # --------------------------------

        policy = self.policy_engine.evaluate(
            transaction,
            strategy["action"]
        )

        result = {
            "transaction_id":
                transaction["transaction_id"],

            "customer_id":
                transaction["customer_id"],

            "amount":
                transaction["amount"],

            "risk_score":
                risk_score,

            "recovery_probability":
                recovery_probability,

            "expected_recoverable_revenue":
                expected_revenue,

            "friction":
                friction,

            "root_cause":
                root_cause,

            "strategy":
                strategy,

            "policy":
                policy,

            "status":
                "PENDING"
        }

        # --------------------------------
        # STEP 5: Execute
        # --------------------------------

        if policy["decision"] != "ALLOW":

            result["status"] = policy["decision"]

            return result

        action = strategy["action"]

        if action == "DELAYED_RETRY":

            execution = (
                self.payment_simulator.retry_payment(
                    transaction
                )
            )

        elif action == "PAYMENT_LINK":

            execution = (
                self.payment_simulator.payment_link(
                    transaction
                )
            )

        elif action == "REMINDER":

            execution = (
                self.payment_simulator.reminder(
                    transaction
                )
            )

        else:

            execution = {
                "success": False,
                "amount": transaction["amount"],
                "message": "NO_AUTO_EXECUTION"
            }

        # --------------------------------
        # STEP 6: Outcome
        # --------------------------------

        result["execution"] = execution

        if execution["success"]:

            result["status"] = "RECOVERED"

            result["recovered_revenue"] = (
                transaction["amount"]
            )

        else:

            result["status"] = "NOT_RECOVERED"

            result["recovered_revenue"] = 0

        return result
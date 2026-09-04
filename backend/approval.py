from datetime import datetime


class ApprovalManager:

    def __init__(self):
        self.approvals = {}

    def create_request(
        self,
        transaction_id,
        amount,
        strategy
    ):

        request = {
            "transaction_id": transaction_id,
            "amount": amount,
            "strategy": strategy,
            "status": "PENDING",
            "created_at": datetime.now().isoformat(),
            "approved_at": None
        }

        self.approvals[transaction_id] = request

        return request

    def approve(self, transaction_id):

        if transaction_id not in self.approvals:

            return {
                "success": False,
                "message": "Approval request not found."
            }

        request = self.approvals[transaction_id]

        if request["status"] != "PENDING":

            return {
                "success": False,
                "message": f"Request already {request['status']}."
            }

        request["status"] = "APPROVED"

        request["approved_at"] = (
            datetime.now().isoformat()
        )

        return {
            "success": True,
            "message": "Recovery approved.",
            "request": request
        }

    def reject(self, transaction_id):

        if transaction_id not in self.approvals:

            return {
                "success": False,
                "message": "Approval request not found."
            }

        request = self.approvals[transaction_id]

        if request["status"] != "PENDING":

            return {
                "success": False,
                "message": f"Request already {request['status']}."
            }

        request["status"] = "REJECTED"

        return {
            "success": True,
            "message": "Recovery rejected.",
            "request": request
        }

    def get_request(self, transaction_id):

        return self.approvals.get(
            transaction_id
        )

    def get_pending_requests(self):

        return [
            request
            for request in self.approvals.values()
            if request["status"] == "PENDING"
        ]
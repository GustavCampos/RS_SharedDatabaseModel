import requests
from schema.query import Query
from schema.mutation import Mutation

class TransactionManagementService:
    def __init__(self, graphql_url: str):
        self.graphql_url = graphql_url

    def create_transaction(self, timestamp: str, transaction_type: str, payer_id: int, receiver_id: int, amount: int) -> dict:
        query = """
        mutation ($timestamp: String!, $transactionType: String!, $payerId: Int!, $receiverId: Int!, $amount: Int!) {
          addTransaction(timestamp: $timestamp, transactionType: $transactionType, payerId: $payerId, receiverId: $receiverId, amount: $amount) {
            id
            timestamp
            transactionType
            payer {
              id
              balance
            }
            receiver {
              id
              balance
            }
            amount
          }
        }
        """
        variables = {
            "timestamp": timestamp,
            "transactionType": transaction_type,
            "payerId": payer_id,
            "receiverId": receiver_id,
            "amount": amount
        }
        return self._execute_query(query, variables)

    def _execute_query(self, query: str, variables: dict) -> dict:
        headers = {"Content-Type": "application/json"}
        data = {
            "query": query,
            "variables": variables
        }
        response = requests.post(self.graphql_url, json=data, headers=headers)
        return response.json()

if __name__ == "__main__":
    transaction_service = TransactionManagementService(graphql_url="http://localhost:5000/graphql")
    
    transaction = transaction_service.create_transaction(
        timestamp="2024-11-26T15:00:00Z", 
        transaction_type="transfer", 
        payer_id=1, 
        receiver_id=2, 
        amount=500
    )
    print(transaction)

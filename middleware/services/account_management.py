import requests
from schema.query import Query
from schema.mutation import Mutation

class AccountManagementService:
    def __init__(self, graphql_url: str):
        self.graphql_url = graphql_url

    def add_account(self, owner_id: int, password: str, balance: int = 0) -> dict:
        query = """
        mutation ($owner: Int!, $password: String!, $balance: Int) {
          addBankAccount(owner: $owner, password: $password, balance: $balance) {
            id
            owner
            balance
          }
        }
        """
        variables = {
            "owner": owner_id,
            "password": password,
            "balance": balance
        }
        return self._execute_query(query, variables)

    def get_account_by_id(self, account_id: int) -> dict:
        query = """
        query ($id: Int!) {
          bankAccount(id: $id) {
            id
            owner
            balance
          }
        }
        """
        variables = {"id": account_id}
        return self._execute_query(query, variables)

    def get_accounts_by_owner(self, owner_id: int) -> dict:
        query = """
        query ($ownerId: Int!) {
          bankAccounts(ownerId: $ownerId) {
            edges {
              node {
                id
                balance
              }
            }
          }
        }
        """
        variables = {"ownerId": owner_id}
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
    account_service = AccountManagementService(graphql_url="http://localhost:5000/graphql")
    
    new_account = account_service.add_account(owner_id=1, password="senha123", balance=1000)
    print(new_account)

    account = account_service.get_account_by_id(account_id=1)
    print(account)

    accounts = account_service.get_accounts_by_owner(owner_id=1)
    print(accounts)

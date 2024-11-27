from .graphql import GraphQLHandler
from ..constants import GRAPHQL_QUERIES

class BankAccountHandler:
    def __init__(self, controller: GraphQLHandler = None) -> None:
        self.controller = controller
    
    def get_accounts(self, **filters) -> dict:
        return self.controller._execute_query(GRAPHQL_QUERIES.bank_accounts, **filters)

    
    def get_account(self, account_id: int):
        # Convert to string to handle bigInt
        str_id = str(account_id)

        return self.controller._execute_query(GRAPHQL_QUERIES.bank_account, id=str_id)
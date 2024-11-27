from .graphql import GraphQLHandler
from ..constants import GRAPHQL_QUERIES

class ClientHandler:
    def __init__(self, controller: GraphQLHandler = None) -> None:
        self.controller = controller
    
    def get_clients(self, name_like: str = "") -> dict:
        return self.controller._execute_query(GRAPHQL_QUERIES.clients, nameLike=name_like)

    
    def get_client(self, client_id: int):
        # Convert to string to handle bigInt
        str_id = str(client_id)

        return self.controller._execute_query(GRAPHQL_QUERIES.client_bank_accounts, id=str_id)
from os.path import realpath
import requests

class GraphQLHandler:
    def __init__(self, graphql_endpoint) -> None:
        self.url = graphql_endpoint
        
    def _execute_query(self, query_file: str, **variables) -> dict | None:
        with open(realpath(query_file), "r") as file:
            query = file.read()
            
        header = {"Content-Type": "application/json"}
        
        payload = {
            "query": query,
            "variables": variables
        }
        
        response = requests.post(self.url, json=payload, headers=header)
        
        if response.status_code == 200:
            return response.json()
        
        return None
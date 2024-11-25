from flask import g
import strawberry
import database.table_model as models
from .query import Client, BankAccount, Transaction
        
        
@strawberry.type
class Mutation():
    @strawberry.mutation
    def add_client(self, info: strawberry.Info, cpf: str, complete_name: str) -> Client:
        session = g.db_session
        
        new_client = models.Client(cpf=cpf, complete_name=complete_name)
        session.add(new_client)
        session.commit()

        return Client(
            id=new_client.id,
            cpf=new_client.cpf,
            complete_name=new_client.complete_name
        )
    
    @strawberry.mutation
    def update_client(self, info: strawberry.Info, cpf: str, complete_name: str) -> Client:
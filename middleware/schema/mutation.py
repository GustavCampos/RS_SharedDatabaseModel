from typing import Optional
import bcrypt
from flask import g
import strawberry
import database.table_model as models
from .query import Client, BankAccount, Transaction
        

@strawberry.type
class Mutation():
    # Client Mutations ____________________________________________________________________________
    @strawberry.mutation
    def add_client(self, info: strawberry.Info, cpf: str, complete_name: str) -> Client:
        session = g.db_session
        
        new_client = models.Client(cpf=cpf, complete_name=complete_name)
        session.add(new_client)
        session.commit()

        return new_client
    
    @strawberry.mutation
    def update_client(self, info: strawberry.Info, id: int, cpf: Optional[str], complete_name: Optional[str]) -> Client:
        session = g.db_session

        client = session.query(models.Client).filter_by(id=id).first()

        if client is None:
            raise ValueError("Client not found")

        if cpf is not None:
            client.cpf = cpf
        if complete_name is not None:
            client.complete_name = complete_name

        session.commit()

        return client
    
    @strawberry.mutation
    def delete_client(self, info:strawberry.Info, id: int) -> Client:
        session = g.db_session

        client = session.query(models.Client).filter_by(id=id).first()

        if client is None:
            raise ValueError("Client not found")

        session.delete(client)
        session.commit()

        return client
    
    # Bank Account Mutations ______________________________________________________________________
    @strawberry.mutation
    def add_bank_account(self, info: strawberry.Info, owner: int, password: str, balance: int = 0) -> BankAccount:
        session = g.db_session
        hash_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(6))
        
        new_bank_account = models.BankAccount(owner=owner, balance=balance, password=hash_pwd)
        session.add(new_bank_account)
        session.commit()

        return new_bank_account


    # Transaction Mutations _______________________________________________________________________
        
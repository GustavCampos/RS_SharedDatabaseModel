from typing import Optional
from flask import g
import strawberry
from strawberry_sqlalchemy_mapper import StrawberrySQLAlchemyMapper
import database.table_model as models


strawberry_sqlalchemy_mapper = StrawberrySQLAlchemyMapper()
@strawberry_sqlalchemy_mapper.type(models.Client)
class Client():
    pass

@strawberry_sqlalchemy_mapper.type(models.BankAccount)
class BankAccount():
    __exclude__ = ["password"]

@strawberry_sqlalchemy_mapper.type(models.Transaction)
class Transaction():
    pass

@strawberry.type
class Query():
    @strawberry.field
    def clients(self, info) -> list[Client]:
        session = g.db_session  
        return session.query(models.Client).all()
    
    @strawberry.field
    def client(self, info: strawberry.Info, id: Optional[int] = None, cpf: Optional[str] = None) -> Optional[Client]:
        session = g.db_session
        
        if id is not None:
            client = session.query(models.Client).filter_by(id=id).first()
        elif cpf is not None:
            client = session.query(models.Client).filter_by(cpf=cpf).first()
        else:
            raise ValueError("You must provide either 'id' or 'cpf'")
        
        if client:
            return Client(
                id=client.id,
                cpf=client.cpf,
                complete_name=client.complete_name
            )
        return None
    
    @strawberry.field
    def bank_accounts(self, info) -> list[BankAccount]:
        session = g.db_session
        return session.query(models.BankAccount).all()
from typing import Optional
from flask import g
import strawberry
from strawberry_sqlalchemy_mapper import StrawberrySQLAlchemyMapper
from sqlalchemy.orm import joinedload
import database.table_model as models


strawberry_sqlalchemy_mapper = StrawberrySQLAlchemyMapper()

@strawberry_sqlalchemy_mapper.type(models.Transaction)
class Transaction():
    pass
@strawberry_sqlalchemy_mapper.type(models.BankAccount)
class BankAccount():
    pass
@strawberry.type
class BankAccountEdge:
    node: BankAccount
@strawberry.type
class BankAccountConnection:
    edges: list[BankAccountEdge]
@strawberry_sqlalchemy_mapper.type(models.Client)
class Client():
    @strawberry.field
    def bank_accounts(self) -> BankAccountConnection:
        accounts = self.bank_accounts
        
        return BankAccountConnection(
            edges=[BankAccountEdge(node=account) for account in accounts]
        )

@strawberry.type
class Query():
    @strawberry.field
    def clients(self, info: strawberry.Info, name_like: Optional[str] = None) -> list[Client]:
        session = info.context["db_session"]

        query = session.query(models.Client)

        if name_like:
            query = query.filter(models.Client.complete_name.like(f"%{name_like}%"))

        return query.all()

    
    @strawberry.field
    def client(self, info: strawberry.Info, id: Optional[int] = None, cpf: Optional[str] = None) -> Optional[Client]:
        session = g.db_session
        
        if id is not None:
            client = session.query(models.Client).filter_by(id=id).first()
        elif cpf is not None:
            client = session.query(models.Client).filter_by(cpf=cpf).first()
        else:
            raise ValueError("You must provide either 'id' or 'cpf'")
        
        return (None, client)[client is not None]
    
    @strawberry.field
    def bank_accounts(self, info, 
        owner_id: Optional[int] = None, 
        owner_cpf: Optional[str] = None, 
        owner_name_like: Optional[str] = None,
        balance_less_than: Optional[int] = None,
        balance_greater_than: Optional[int] = None
    ) -> list[BankAccount]:
        session = g.db_session

        query = session.query(models.BankAccount)

        if owner_id:
            query = query.filter(models.BankAccount.owner == owner_id)
        elif owner_cpf:
            query = query.filter(models.BankAccount.owner_obj.cpf == owner_cpf)
        elif owner_name_like:
            query = query.filter(models.BankAccount.owner_obj.complete_name.like(f"%{owner_name_like}%"))

        if balance_less_than:
            query = query.filter(models.BankAccount.balance < balance_less_than)
        if balance_greater_than:
            query = query.filter(models.BankAccount.balance > balance_greater_than)

        return query.all()
    
    @strawberry.field
    def bank_account(self, info: strawberry.Info, id: int) -> Optional[BankAccount]:
        session = g.db_session
        account = session.query(models.BankAccount).filter_by(id=id).first()
        return (None, account)[account is not None]
    
    @strawberry.field
    def transactions(self, info: strawberry.Info,
        transaction_type: Optional[str] = None,
        # timestamp filters
        datetime_less_than: Optional[str] = None,
        datetime_greater_than: Optional[str] = None,
        # amount filters
        amount_less_than: Optional[int] = None,
        amount_greater_than: Optional[int] = None,
        # Payer filters
        payer_id: Optional[int] = None,
        payer_account: Optional[int] = None,
        payer_name_like: Optional[str] = None,
        payer_cpf: Optional[str] = None,
        # Receiver filters
        receiver_id: Optional[int] = None,
        receiver_account: Optional[int] = None,
        receiver_name_like: Optional[str] = None,
        receiver_cpf: Optional[str] = None,

    ) -> list[Transaction]:
        session = g.db_session

        query = session.query(models.Transactions)

        if transaction_type:
            query = query.filter(models.Transaction.transaction_type == transaction_type)
        if datetime_less_than:
            query = query.filter(models.Transaction.timestamp < datetime_less_than)
        if datetime_greater_than:
            query = query.filter(models.Transaction.timestamp < datetime_greater_than)
        if amount_less_than:
            query = query.filter(models.Transaction.amount < amount_less_than)
        if amount_greater_than:
            query = query.filter(models.Transaction.amount > amount_greater_than)
        if payer_id:
            query = query.filter(models.Transaction.payer_obj.owner_obj.id == payer_id)
        if payer_account:
            query = query.filter(models.Transaction.payer == payer_account)
        if payer_name_like:
            query = query.filter(models.Transaction.payer_obj.owner_obj.complete_name.like(f"%{payer_name_like}%"))
        if payer_cpf:
            query = query.filter(models.Transaction.payer_obj.owner_obj.cpf == payer_cpf)
        if receiver_id:
            query = query.filter(models.Transaction.receiver_obj.owner_obj.id == receiver_id)
        if receiver_account:
            query = query.filter(models.Transaction.receiver == receiver_account)        
        if receiver_name_like:
            query = query.filter(models.Transaction.receiver_obj.owner_obj.complete_name.like(f"%{receiver_name_like}%"))
        if receiver_cpf:
            query = query.filter(models.Transaction.receiver_obj.owner_obj.cpf == receiver_cpf)

        return query.all()

    @strawberry.field
    def transaction(self, info: strawberry.Info, id: int) -> Optional[Transaction]:
        session = g.db_session
        transaction = session.query(models.Transaction).filter_by(id=id).first()
        return (None, transaction)[transaction is not None]
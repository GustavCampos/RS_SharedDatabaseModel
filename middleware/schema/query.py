import strawberry
import database.table_model as models 
from typing import Optional
from .model import Client, BankAccount, Transaction, BigInt


@strawberry.type
class Query:
    @strawberry.field
    def clients(self, info: strawberry.Info, name_like: Optional[str] = None) -> list[Client]:
        session = info.context["db_session"]

        query = session.query(models.Client)

        if name_like:
            query = query.filter(models.Client.complete_name.like(f"%{name_like}%"))

        return query.all()

    
    @strawberry.field
    def client(self, info: strawberry.Info, id: Optional[BigInt] = None, cpf: Optional[str] = None) -> Optional[Client]:
        session = info.context["db_session"]

        query = session.query(models.Client)

        if id is not None:
            query = query.filter_by(id=id)
        elif cpf is not None:
            query = query.filter_by(cpf=cpf)
        else:
            query = query.filter_by(id=1)
                    
        return query.first()
    
    @strawberry.field
    def bank_accounts(self, info, 
        owner_id: Optional[BigInt] = None, 
        owner_cpf: Optional[str] = None, 
        owner_name_like: Optional[str] = None,
        balance_less_than: Optional[BigInt] = None,
        balance_greater_than: Optional[BigInt] = None
    ) -> list[BankAccount]:
        session = info.context["db_session"]

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
    def bank_account(self, info: strawberry.Info, id: BigInt=1) -> Optional[BankAccount]:
        session = info.context["db_session"]
        
        query = session.query(models.BankAccount).filter_by(id=id)
        
        return query.first()
    
    @strawberry.field
    def transactions(self, info: strawberry.Info,
        transaction_type: Optional[str] = None,
        # timestamp filters
        datetime_less_than: Optional[str] = None,
        datetime_greater_than: Optional[str] = None,
        # amount filters
        amount_less_than: Optional[BigInt] = None,
        amount_greater_than: Optional[BigInt] = None,
        # Payer filters
        payer_id: Optional[BigInt] = None,
        payer_account: Optional[BigInt] = None,
        payer_name_like: Optional[str] = None,
        payer_cpf: Optional[str] = None,
        # Receiver filters
        receiver_id: Optional[BigInt] = None,
        receiver_account: Optional[BigInt] = None,
        receiver_name_like: Optional[str] = None,
        receiver_cpf: Optional[str] = None,

    ) -> list[Transaction]:
        session = info.context["db_session"]

        query = session.query(models.Transaction)

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
    def transaction(self, info: strawberry.Info, id: BigInt) -> Optional[Transaction]:
        session = info.context["db_session"]
        
        query = session.query(models.Transaction).filter_by(id=id)
        
        return query.first()
    
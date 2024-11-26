import bcrypt
import strawberry
import database.table_model as models
from datetime import datetime
from typing import Optional
from schema.model import TransactionType
from .query import Client, BankAccount, Transaction


SALT_ROUNDS = 6
DISSOLVE_LIMIT = 300 # Value in seconds
CLIENT_NOT_FOUND_MSG = "Client not found"

@strawberry.type
class Mutation():
    # Client Mutations ____________________________________________________________________________
    @strawberry.mutation
    def add_client(self, info: strawberry.Info, cpf: str, complete_name: str) -> Client:
        session = info.context["db_session"]
        
        try:
            new_client = models.Client(cpf=cpf, complete_name=complete_name)
            session.add(new_client)
            session.commit()

            return new_client
        
        except Exception as e:
            session.rollback()
            return e
    
    @strawberry.mutation
    def update_client(self, info: strawberry.Info, id: int, cpf: Optional[str], complete_name: Optional[str]) -> Client:
        session = info.context["db_session"]
        
        try:
            client = session.query(models.Client).filter_by(id=id).first()

            if client is None:
                raise ValueError(CLIENT_NOT_FOUND_MSG)

            if cpf is not None:
                client.cpf = cpf
            if complete_name is not None:
                client.complete_name = complete_name

            session.commit()

            return client
        
        except Exception as e:
            session.rollback()
            return e
    
    @strawberry.mutation
    def delete_client(self, info:strawberry.Info, id: int) -> Client:
        session = info.context["db_session"]

        try:
            client = session.query(models.Client).filter_by(id=id).first()

            if client is None:
                raise ValueError(CLIENT_NOT_FOUND_MSG)

            # Verify if all bank accounts are empty to cascade delete
            bank_accounts = session.query(models.BankAccount).filter_by(owner=id).all()
            
            for account in bank_accounts:
                if account.balance != 0:
                    raise ValueError("Cannot delete client with non-empty bank accounts")
            
                session.delete(account)
            
            session.delete(client)
            session.commit()

            return client
        
        except Exception as e:
            session.rollback()
            return e
    
    # Bank Account Mutations ______________________________________________________________________
    @strawberry.mutation
    def add_bank_account(self, info: strawberry.Info, owner: int, password: str, balance: int = 0) -> BankAccount:
        session = info.context["db_session"]
        
        try:
            hash_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(SALT_ROUNDS))
            
            new_bank_account = models.BankAccount(owner=owner, balance=balance, password=hash_pwd)
            session.add(new_bank_account)
            session.commit()

            return new_bank_account
        
        except Exception as e:
            session.rollback()
            return e
    
    def update_bank_account(self, info:strawberry.Info, id: int, password: str) -> BankAccount:
        session = info.context["db_session"]
        
        try:
            hash_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(SALT_ROUNDS))
            
            account = session.query(models.BankAccount).filter_by(id=id).first()

            if account is None:
                raise ValueError("Account not found")

            account.password = hash_pwd
            session.commit()

            return account
        
        except Exception as e:
            session.rollback()
            return e
    
    @strawberry.mutation
    def delete_bank_account(self, info:strawberry.Info, id: int) -> Client:
        session = info.context["db_session"]

        try:
            account = session.query(models.BankAccount).filter_by(id=id).first()

            if account is None:
                raise ValueError("Client not found")

            session.delete(account)
            session.commit()

            return account
        
        except Exception as e:
            session.rollback()
            return e


    # Transaction Mutations _______________________________________________________________________
    @strawberry.mutation
    def add_transaction(self, info: strawberry.Info, type: TransactionType, amount: int, payer: Optional[int] = None, receiver: Optional[int] = None) -> Transaction:
        session = info.context["db_session"]
        
        try:
            payer_obj = None
            if type in (TransactionType.WITHDRAWAL, TransactionType.TRANSFER):
                if payer is None:
                    raise ValueError(f"Payer argument needed for {type} transaction")
                
                payer_obj = session.query(models.BankAccount).filter_by(id=payer).first()
                
                if payer_obj is None:
                    raise ValueError("Payer does not exist in database")
                
                payer_obj.balance = (int(payer_obj.balance) - int(amount))
                
            receiver_obj = None
            if type in (TransactionType.DEPOSIT, TransactionType.TRANSFER):
                if receiver is None:
                    raise ValueError(f"Receiver argument needed for {type} transaction")
                
                receiver_obj = session.query(models.BankAccount).filter_by(id=receiver).first()
                
                if receiver_obj is None:
                    raise ValueError("Receiver does not exist in database")
                
                receiver_obj.balance = (int(receiver_obj.balance) + int(amount))
                
            transaction = models.Transaction(
                timestamp=datetime.now(),
                transaction_type=type.value,
                payer=payer_obj.id,
                receiver=receiver_obj.id,
                amount=amount
            )
            
            session.add(transaction)
            session.commit()
            
            return transaction
            
        except Exception as e:
            session.rollback()
            return e
        
    @strawberry.mutation
    def dissolve_transaction(self, info: strawberry.Info, id: int) -> Transaction:
        session = info.context["db_session"]

        try:
            transaction = session.query(models.Transaction).filter_by(id=id).first()
            if transaction is None:
                raise ValueError("Transaction not found")
            
            if (datetime.now() - transaction.timestamp).seconds > DISSOLVE_LIMIT:
                raise ValueError(f"Transaction cannot be dissolved after {(DISSOLVE_LIMIT / 60)} minutes")
            
            t_type = transaction.transaction_type
            
            
            if t_type in (TransactionType.WITHDRAWAL, TransactionType.TRANSFER):
                payer = session.query(models.BankAccount).filter_by(id=transaction.payer).first()
                
                if payer is None:
                    raise ValueError(f"{t_type.capitalize()} transaction does not have a valid payer anymore")
                
                payer.balance = (int(payer.balance) + int(transaction.amount))
            
            if t_type in (TransactionType.DEPOSIT, TransactionType.TRANSFER):
                receiver = session.query(models.BankAccount).filter_by(id=transaction.receiver).first()
                
                if receiver is None:
                    raise ValueError(f"{t_type.capitalize()} transaction does not have a valid receiver anymore")

                receiver.balance = (int(receiver.balance) - int(transaction.amount))

            session.delete(transaction)
            session.commit()
            
            return transaction
            
        except Exception as e:
            session.rollback()
            return e
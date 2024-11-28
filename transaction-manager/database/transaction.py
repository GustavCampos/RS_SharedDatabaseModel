from multiprocessing import Value
from typing import List

import bcrypt
from database.operations import OperationHandler, read_operation, write_operation
from sqlalchemy.orm import Session
from database.table_model import Transaction, BankAccount
from datetime import datetime, timezone


class TransactionHandler(OperationHandler):
    def _handle_deposit(self, amount: float, receiver_id: int, password: str, db_session: Session):
        if not receiver_id or not password:
            raise ValueError("Receiver ID and password are required for deposit")
            
        receiver = db_session.query(BankAccount).filter_by(id=receiver_id).first()
        
        if not receiver:
            raise ValueError("Invalid receiver ID")
        
        if not bcrypt.checkpw(password.encode(), receiver.password.encode()):
            raise ValueError("Invalid password for transaction")
        
        receiver.balance += amount

    def _handle_withdrawal(self, amount: float, payer_id: int, password: str, db_session: Session):
        if not payer_id or not password:
            raise ValueError("Payer ID and password are required for withdrawal")
        
        payer = db_session.query(BankAccount).filter_by(id=payer_id).first()
        
        if not payer:
            raise ValueError("Invalid payer ID or password")
        
        if not bcrypt.checkpw(password.encode(), payer.password.encode()):
            raise ValueError("Invalid password for transaction")
        
        if payer.balance < amount:
            raise ValueError("Insufficient funds")
        
        payer.balance -= amount

    def _handle_transaction(self, amount: float, payer_id: int, receiver_id: int, password: str, db_session: Session):
        if not payer_id or not receiver_id or not password:
            raise ValueError("Payer ID, receiver ID, and password are required for transaction")
        
        payer = db_session.query(BankAccount).filter_by(id=payer_id).first()
        receiver = db_session.query(BankAccount).filter_by(id=receiver_id).first()
        
        if not payer:
            raise ValueError("Invalid payer ID or password")
        
        if not receiver:
            raise ValueError("Invalid receiver ID")
        
        if not bcrypt.checkpw(password.encode(), payer.password.encode()):
            raise ValueError("Invalid password for transaction")
        
        if payer.balance < amount:
            raise ValueError("Insufficient funds")
        
        payer.balance -= amount
        receiver.balance += amount

    # Read operations _____________________________________________________________
    @read_operation
    def get_transaction(self, transaction_id: int, db_session: Session = None) -> Transaction:
        transaction = db_session.query(
            Transaction).filter_by(id=transaction_id).first()
        return {
            "id": transaction.id,
            "amount": transaction.amount,
            "timestamp": transaction.timestamp,
            "version": transaction.version
        }

    @read_operation
    def list_transactions(self, account_id: int = None, db_session: Session = None) -> List[Transaction]:
        query = db_session.query(Transaction)
        if account_id:
            query = query.filter((Transaction.payer == account_id) | (Transaction.receiver == account_id))
        return query.all()

    # Write operations ____________________________________________________________
    @write_operation
    def create_transaction(self, transaction_type: str, amount: float, payer_id: int = None, receiver_id: int = None, password: str = None, payer_version: int = None, receiver_version: int = None, db_session: Session = None):
        if transaction_type not in ["deposit", "withdrawal", "transaction"]:
            raise ValueError("Invalid transaction type")

        if transaction_type == "deposit":
            receiver = db_session.query(BankAccount).filter_by(id=receiver_id).first()
            
            if receiver.version != receiver_version:
                raise ValueError("Receiver account version mismatch")
            
            self._handle_deposit(amount, receiver_id, password, db_session)
        
        elif transaction_type == "withdrawal":
            payer = db_session.query(BankAccount).filter_by(id=payer_id).first()
            
            if payer.version != payer_version:
                raise ValueError("Payer account version mismatch")
            
            self._handle_withdrawal(amount, payer_id, password, db_session)
        
        elif transaction_type == "transaction":
            payer = db_session.query(BankAccount).filter_by(id=payer_id).first()
            receiver = db_session.query(BankAccount).filter_by(id=receiver_id).first()
            
            if payer.version != payer_version:
                raise ValueError("Payer account version mismatch")
            
            if receiver.version != receiver_version:
                raise ValueError("Receiver account version mismatch")
            
            self._handle_transaction(amount, payer_id, receiver_id, password, db_session)

        db_session.flush()

        new_transaction = Transaction(
            amount=amount, 
            timestamp=datetime.now(timezone.utc),
            transaction_type=transaction_type, 
            payer=payer_id, 
            receiver=receiver_id
        )
        
        db_session.add(new_transaction)
        db_session.flush()  # Ensure the instance is bound to the session

        return {
            "id": new_transaction.id,
            "amount": new_transaction.amount,
            "timestamp": new_transaction.timestamp,
            "version": new_transaction.version,
            "transaction_type": new_transaction.transaction_type,
            "payer_id": new_transaction.payer,
            "receiver_id": new_transaction.receiver
        }


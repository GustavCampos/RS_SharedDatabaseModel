from typing import List
from database.operations import OperationHandler, read_operation, write_operation
from database.table_model import Client, BankAccount
from sqlalchemy.orm import Session
from prettytable import PrettyTable


class ClientHandler(OperationHandler):
    # Read operations _____________________________________________________________
    @read_operation
    def get_client(self, client_id: int, db_session: Session = None) -> Client:
        client = db_session.query(Client).filter_by(id=client_id).first()
        return {
            "id": client.id,
            "cpf": client.cpf,
            "complete_name": client.complete_name,
            "version": client.version
        }
        
        
    @read_operation
    def list_client(self, owner_id: int = None, db_session: Session = None) -> List[Client]:
        return db_session.query(Client).all()

    # Write operations ____________________________________________________________
    @write_operation
    def create_client(self, cpf: str, complete_name: str, db_session: Session = None):
        new_client = Client(cpf=cpf, complete_name=complete_name)
        db_session.add(new_client)
        db_session.flush()  # Ensure the instance is bound to the session
        return {
            "id": new_client.id,
            "cpf": new_client.cpf,
            "complete_name": new_client.complete_name,
            "version": new_client.version
        }
        
    @write_operation
    def update_client(self, client_id: int, cpf: str = None, complete_name: str = None, db_session: Session = None):
        client = db_session.query(Client).filter_by(id=client_id).first()
        
        if not client:
            raise ValueError("User with provided id does not exist on database")
        
        if cpf:
            client.cpf = cpf
        if complete_name:
            client.complete_name = complete_name
            
        client.version += 1
        db_session.flush()  # Ensure the instance is bound to the session
        
        return {
            "id": client.id,
            "cpf": client.cpf,
            "complete_name": client.complete_name,
            "version": client.version
        }

    @write_operation
    def delete_client(self, client_id: int, db_session: Session = None):
        client = db_session.query(Client).filter_by(id=client_id).first()
        
        if not client:
            raise ValueError("User with provided id does not exist on database")
        
        # Verify if all client bank accounts are with balance == 0
        accounts = db_session.query(BankAccount).filter_by(owner=client_id).all()
        for account in accounts:
            if account.balance != 0:
                raise ValueError("All client bank accounts must have a balance of 0 before deletion")
        
        # Delete all client bank accounts
        for account in accounts:
            db_session.delete(account)
        
        db_session.flush()  # Ensure the instance is bound to the session
        
        # Delete the client
        db_session.delete(client)
        db_session.flush()  # Ensure the instance is bound to the session
        
        return {
            "id": client.id,
            "cpf": client.cpf,
            "complete_name": client.complete_name,
            "version": client.version
        }

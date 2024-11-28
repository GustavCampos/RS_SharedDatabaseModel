import bcrypt
from filelock import FileLock
from sqlalchemy.orm import Session, sessionmaker
from database.operations import OperationHandler, write_operation, read_operation
from .table_model import BankAccount

class AccountHandler(OperationHandler):
    def __init__(self, filelock: FileLock, pwd_salt: int = 6) -> None:
        super().__init__(filelock)
        self.pwd_salt = pwd_salt
    
    # Read operations _____________________________________________________________
    @read_operation
    def get_account(self, account_id: int, db_session: Session = None):
        account = db_session.query(BankAccount).filter_by(id=account_id).first()
    
        return {
                "id": account.id,
                "owner": account.owner,
                "password": account.password,
                "version": account.version
        }
        
    @read_operation
    def list_account(self, owner_id: int = None, db_session: Session = None):
        return db_session.query(BankAccount).all()

    # Write operations ____________________________________________________________
    @write_operation
    def create_account(self, owner_id: int, password: str, db_session: Session = None):
        hash_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(self.pwd_salt))
        new_account = BankAccount(owner=owner_id, password=hash_pwd)
        db_session.add(new_account)
        db_session.flush()  # Ensure the instance is bound to the session
        
        return {
            "id": new_account.id,
            "owner": new_account.owner,
            "password": new_account.password,
            "version": new_account.version
        }
        
    @write_operation
    def update_account(self, account_id: int, owner_id: int = None, password: str = None, db_session: Session = None):
        account = db_session.query(BankAccount).filter_by(id=account_id).first()
        
        if not account:
            raise ValueError("Account with provided id does not exist on database")
        
        if owner_id:
            account.owner = owner_id
        if password:
            hash_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(self.pwd_salt))
            account.password = hash_pwd
            
        account.version += 1
        db_session.flush()  # Ensure the instance is bound to the session
        
        return {
            "id": account.id,
            "owner": account.owner,
            "password": account.password,
            "version": account.version
        }

    @write_operation
    def delete_account(self, account_id: int, db_session: Session = None):
        account = db_session.query(BankAccount).filter_by(id=account_id).first()
        
        if not account:
            raise ValueError("Account with provided id does not exist on database")
        
        db_session.delete(account)
        db_session.flush()  # Ensure the instance is bound to the session
        
        return {
            "id": account.id,
            "owner": account.owner,
            "password": account.password,
            "version": account.version
        }
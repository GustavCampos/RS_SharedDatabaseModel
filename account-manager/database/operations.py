from filelock import FileLock
from sqlalchemy.orm import sessionmaker
from functools import wraps


class OperationHandler:
    def __init__(self, sessionmaker: sessionmaker, filelock: FileLock) -> None:
        self.sessionmaker = sessionmaker
        self.filelock = filelock

def write_operation(operation_func):
    @wraps(operation_func)
    def wrapper(self, *args, **kwargs):
        filelock = getattr(self, "filelock")
        sessionmaker = getattr(self, "sessionmaker")
        
        with filelock:
            session = sessionmaker()
            
            try:
                # Evaluates if operation steps were correctly made
                result = operation_func(self, *args, db_session=session, **kwargs)
                session.commit()
                
            except Exception as e:
                print(f"Something occured, rollbacking...: {e}")
                session.rollback()
                raise e
            
            finally:
                session.remove()
                
        return result
    return wrapper

def read_operation(operation_func):
    @wraps(operation_func)
    def wrapper(self, *args, **kwargs):
        sessionmaker = getattr(self, "sessionmaker")
        session = sessionmaker()
        
        result = operation_func(self, *args, db_session=session, **kwargs)
        
        session.remove()
        
        return result
    return wrapper
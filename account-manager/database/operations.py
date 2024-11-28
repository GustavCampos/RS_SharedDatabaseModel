import os
from filelock import FileLock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from functools import wraps

from database.table_model import get_declarative_base

DB_PATH = os.getenv("DATABASE_PATH")
if not DB_PATH:
    raise EnvironmentError("DATABASE_PATH environment variable is not set")

DB_FILE = os.path.realpath(DB_PATH)
LOCK_FILE = f"{DB_FILE}.lock"

def get_engine():
    return create_engine(f"duckdb:///{DB_FILE}")

def create_access(create_table=False):
    engine = get_engine()
    sqa_base = get_declarative_base()
    
    smaker = scoped_session(
        sessionmaker(
            bind=engine, 
            autocommit=False, 
            autoflush=False
        )
    )
    
    if create_table:
        sqa_base.metadata.create_all(bind=engine)
    
    sqa_base.metadata.reflect(bind=engine) # Load metadata 
    
    return [engine, smaker]

class OperationHandler:
    def __init__(self, filelock: FileLock) -> None:
        self.filelock = filelock

def write_operation(operation_func):
    @wraps(operation_func)
    def wrapper(self, *args, **kwargs):
        filelock = getattr(self, "filelock")

        engine, smaker = create_access()
        
        with filelock:
            session = smaker()
            
            try:
                # Evaluates if operation steps were correctly made
                result = operation_func(self, *args, db_session=session, **kwargs)
                session.commit()
                
            except Exception as e:
                print(f"Something occured, rollbacking...: {e}")
                session.rollback()
                raise e
            
            finally:
                smaker.remove()
                engine.dispose()  # Dispose of the engine here
                
        return result
    return wrapper

def read_operation(operation_func):
    @wraps(operation_func)
    def wrapper(self, *args, **kwargs):
        engine, smaker = create_access()
        session = smaker()
        
        result = operation_func(self, *args, db_session=session, **kwargs)
        
        smaker.remove()
        engine.dispose()  # Dispose of the engine here
        
        return result
    return wrapper
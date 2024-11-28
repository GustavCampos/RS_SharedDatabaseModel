import os
from cli import AccountManagerCLI
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from database.table_model import get_declarative_base
from dotenv import load_dotenv
from filelock import FileLock

load_dotenv()

# Database setup __________________________________________________________________________________
DB_FILE = os.path.realpath(os.getenv("DATABASE_PATH"))
LOCK_FILE = f"{DB_FILE}.lock"

ENGINE = create_engine(f"duckdb:///{DB_FILE}")
FILELOCK = FileLock(LOCK_FILE, timeout=10)

SQA_BASE = get_declarative_base()
SESSION_MAKER = scoped_session(
    sessionmaker(
        bind=ENGINE, 
        autocommit=False, 
        autoflush=False
    )
)

# Main code _______________________________________________________________________________________
if __name__ == "__main__":
    SQA_BASE.metadata.create_all(bind=ENGINE) # Create tables in case not exist
    SQA_BASE.metadata.reflect(bind=ENGINE) # Load metadata
    
    AccountManagerCLI(SESSION_MAKER, FILELOCK).cmdloop()
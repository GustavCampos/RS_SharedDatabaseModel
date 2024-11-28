import os
from filelock import FileLock
from cli import AccountManagerCLI
from database.operations import create_access
from dotenv import load_dotenv

load_dotenv()

# Database setup __________________________________________________________________________________
DB_FILE = os.path.realpath(os.getenv("DATABASE_PATH"))
LOCK_FILE = f"{DB_FILE}.lock"
FILELOCK = FileLock(LOCK_FILE, timeout=10)

ENGINE, SESSIONMAKER = create_access(create_table=True)
ENGINE.dispose()

# Main code _______________________________________________________________________________________
if __name__ == "__main__":
    AccountManagerCLI(FILELOCK).cmdloop()
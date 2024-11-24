import os
from sqlalchemy import create_engine
from table_model import Base
from sqlalchemy.orm import sessionmaker


def get_database_engine(db: str ="duckdb"):
    db_path = os.path.realpath(os.getenv("DATABASE_PATH"))
    
    return create_engine(f"{db}///{db_path}")

def get_declarative_base(engine):
    """_summary_
    Get a declarative base with engine binded and metadata loaded

    Args:
        engine: SQLAlchemy database engine

    Returns:
        Base: declarative base obj
    """
    
    Base.metadata.bind = engine # Bind engine to metadata
    Base.metadata.create_all(engine) # Create tables in case not exist
    Base.metadata.reflect() # Load metadata
    
    return Base

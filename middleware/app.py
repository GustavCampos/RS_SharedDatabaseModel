import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_graphene3 import GraphQLApp
from sqlalchemy.orm import sessionmaker
from database import get_database_engine
from schema.query import get_graphql_schema

# Load env files on development
load_dotenv()

# Constants
DEBUG_MODE = bool(int(os.getenv("DEBUG_MODE")))
SESSION_MAKER = sessionmaker(
    bind=get_database_engine(), 
    autocommit=False, 
    autoflush=False
)

def get_session():
    db = SESSION_MAKER()
    try:
        yield db
    finally:
        db.close()

app = FastAPI() # Create App
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_route("/graphql", 
    GraphQLApp(
        schema=get_graphql_schema(), 
        context_value={'session': get_session}
    )
)

@app.teardown_appcontext
def shutdown_session(exception=None):
    SESSION_MAKER.close_all()

if __name__ == "__main__":
    app.run(debug=DEBUG_MODE)
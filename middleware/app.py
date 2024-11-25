import os
from dotenv import load_dotenv
from flask import Flask, g
from flask_cors import CORS
from sqlalchemy import create_engine
from database import get_declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from schema import CustomGraphQLView, get_graphql_schema


# Load env files on development
load_dotenv()

# Constants
DEBUG_MODE = bool(int(os.getenv("FLASK_DEBUG")))
ENGINE = create_engine("duckdb:///" + os.path.realpath(os.getenv("DATABASE_PATH")))
SQA_BASE = get_declarative_base()
SESSION_MAKER = scoped_session(
    sessionmaker(
        bind=ENGINE, 
        autocommit=False, 
        autoflush=False
    )
)

# # Setup database
SQA_BASE.metadata.create_all(bind=ENGINE) # Create tables in case not exist
SQA_BASE.metadata.reflect(bind=ENGINE) # Load metadata

app = Flask(__name__) # Create App
CORS(app) # Allow CORS

@app.before_request
def before_request():
    g.db_session = SESSION_MAKER()

@app.teardown_request
def teardown_request(exception=None):
    if hasattr(g, 'db_session'):
        g.db_session.close()

app.add_url_rule("/graphql", methods=["POST"],
    view_func=CustomGraphQLView.as_view(
        name="graphql_view",
        schema=get_graphql_schema(),
        graphiql=True
    )
)
    
if __name__ == "__main__":
    app.run(debug=DEBUG_MODE)
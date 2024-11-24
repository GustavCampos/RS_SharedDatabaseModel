import os
from database.table_model import GetDeclarativeBase
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schema.query import GraphQLSchema

# Load env files on development
load_dotenv()

# Constants
DEBUG_MODE = False
db_engine = create_engine("duckdb:///" + os.path.realpath(os.getenv("DATABASE_PATH")))
sqa_base = GetDeclarativeBase()
gql_schema = GraphQLSchema()

# Initial Execution
sqa_base.metadata.create_all(db_engine) # Create tables if not exist
db_session = sessionmaker(bind=db_engine, autocommit=False, autoflush=False)() # Create database session

app = Flask(__file__) # Create Flask App
CORS(app) # Enable CORS

app.add_url_rule("/graphql", 
    view_func=GraphQLView.as_view("graphql", 
        schema=gql_schema, 
        graphiql=True
    )
)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.close()

if __name__ == "__main__":
    app.run(debug=DEBUG_MODE)
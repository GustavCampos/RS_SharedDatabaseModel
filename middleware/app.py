import os
from database.table_model import Base
from dotenv import load_dotenv
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

# Load env files on development
load_dotenv()

DEBUG_MODE = False
DB_ENGINE = create_engine("duckdb:///" + os.path.realpath(os.getenv("DATABASE_PATH")))

# Initial Execution
Base.metadata.create_all(DB_ENGINE) # Create tables if not exist
db_session = sessionmaker(bind=DB_ENGINE)() # Create database session
app = Flask(__file__) # Create Flask App
CORS(app) # Enable CORS

@app.route("/graphql", methods=["GET"])
def graphql_handler():
    # Load database metadata
    print(inspect(DB_ENGINE).get_table_names())
        
    response = make_response(jsonify({"jorge": "jorge"}), 200)
    response.headers["Content-Type"] = "application/graphql-response+json"
        
    return response

if __name__ == "__main__":
    app.run(debug=DEBUG_MODE)
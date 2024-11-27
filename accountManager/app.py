from flask import Flask, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from src import register_routes
from src.constants import GLOBAL_VARIABLES

load_dotenv()

app = Flask(__name__)
CORS(app)
register_routes(app)

@app.context_processor
def inject_global_variables():
    return GLOBAL_VARIABLES

@app.route("/")
def app_index():
    return render_template("index.jinja")

if __name__ == "__main__":
    app.run()   
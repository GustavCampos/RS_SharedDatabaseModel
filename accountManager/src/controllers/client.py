import os
from flask import Blueprint, render_template
from ..handlers.client import ClientHandler
from ..handlers.graphql import GraphQLHandler
from ..constants import GLOBAL_VARIABLES as GV

client_bp = Blueprint("client", __name__)
handler = ClientHandler(GraphQLHandler(os.getenv("DB_API_URL")))

@client_bp.route(GV["URL"]["CLIENTS"]["LIST"])
def get_clients():
    response = handler.get_clients()
    
    if response is None:
        raise ValueError("Empty response from handler.get_clients()")
    
    table_obj = {
        "headers": ["ID", "Name", "CPF"],
        "rows": [{
            "ID": client["id"],
            "Name": client["completeName"],
            "CPF": client["cpf"],
            "URL": f"{GV["URL"]["CLIENTS"]["LIST"]}/{client["id"]}",
        } for client in response["data"]["clients"]],
        "url_key": "URL",
        "mask": {
            "CPF": "cpf"
        }
    }
    
    return render_template("pages/clients.jinja",
        clients_table=table_obj
    )
    
@client_bp.route(f"{GV["URL"]["CLIENTS"]["LIST"]}/<client_id>")
def get_client(client_id):
    return handler.get_client(client_id)
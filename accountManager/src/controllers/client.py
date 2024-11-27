import os
from flask import Blueprint, render_template
from ..handlers.client import ClientHandler
from ..handlers.graphql import GraphQLHandler
from ..constants import GLOBAL_VARIABLES as GV

client_bp = Blueprint("client", __name__)
handler = ClientHandler(GraphQLHandler(os.getenv("DB_API_URL")))

# flask app
@client_bp.route(GV["URL"]["CLIENTS"]["LIST"])
def get_clients():
    response = handler.get_clients()
    
    if response is None:
        raise ValueError("Empty response from handler.get_clients()")
    
    table_obj = {
        "name": "Client List",
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
        },
        "create_button": {
            "text": "Create Client",
            "url": GV["URL"]["CLIENTS"]["CREATE"],
            "icon": "fa-solid fa-user-plus"
        }
    }
    
    return render_template("pages/client/list.jinja",
        clients_table=table_obj
    )
    
@client_bp.route(f"{GV["URL"]["CLIENTS"]["LIST"]}/<client_id>")
def get_client(client_id):
    response = handler.get_client(client_id)
    
    if response is None:
        raise ValueError("Empty response from handler.get_client()")
        
    client = response["data"]["client"]
    
    accounts = client.pop("bankAccounts")
    accounts_table = {
        "name": f"{client["completeName"]} Accounts",
        "headers": ["ID", "Balance"],
        "rows": [{
            "ID": a["id"],
            "Balance": a["balance"],
            "URL": f"{GV["URL"]["BANK_ACCOUNTS"]["LIST"]}/{a["id"]}",
        } for a in accounts],
        "url_key": "URL",
        "mask": {
            "Balance": "currency"
        },
        "create_button": {
            "text": "Create Account",
            "url": GV["URL"]["BANK_ACCOUNTS"]["CREATE"],
            "icon": "fa-solid fa-plus"
        }
    }
    
    
    return render_template("pages/client/client.jinja",
        client=client,
        bank_accounts_table=accounts_table
    )
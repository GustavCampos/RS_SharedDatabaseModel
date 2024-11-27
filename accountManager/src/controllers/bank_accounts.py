import os
from flask import Blueprint, render_template
from ..handlers.bank_account import BankAccountHandler
from ..handlers.graphql import GraphQLHandler
from ..constants import GLOBAL_VARIABLES as GV

bank_account_bp = Blueprint("bank_account", __name__)
handler = BankAccountHandler(GraphQLHandler(os.getenv("DB_API_URL")))

@bank_account_bp.route(GV["URL"]["BANK_ACCOUNTS"]["LIST"])
def get_accounts():
    response = handler.get_accounts()
    
    if response is None:
        raise ValueError("Empty response from handler.get_accounts()")
    
    account_table = {
        "name": "Bank Account List",
        "headers": ["ID", "Client ID", "Client Name"],
        "rows": [{
            "ID": a["id"],
            "Client ID": a["ownerObj"]["id"],
            "Client Name": a["ownerObj"]["completeName"],
            "URL": f"{GV["URL"]["BANK_ACCOUNTS"]["LIST"]}/{a["id"]}",
        } for a in response["data"]["bankAccounts"]],
        "url_key": "URL",
        "create_button": {
            "text": "Create Bank Account",
            "url": GV["URL"]["BANK_ACCOUNTS"]["CREATE"],
            "icon": "fa-solid fa-plus"
        }
    }
    
    return render_template("pages/bank_account/list.jinja",
        bank_accounts_table=account_table
    )

@bank_account_bp.route(f"{GV["URL"]["BANK_ACCOUNTS"]["LIST"]}/<account_id>")
def get_account(account_id):
    response = handler.get_account(account_id)
    
    print(response)
    
    if response is None:
        raise ValueError("Empty response from handler.get_client()")
    
    account = response["data"]["bankAccount"]
    client = account.pop("ownerObj")
    
    return render_template("pages/bank_account/bank_account.jinja",
        client=client
    )
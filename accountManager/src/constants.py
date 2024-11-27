GLOBAL_VARIABLES = {
    "URL": {
        "ROOT": "/",
        "CLIENTS": {
            "LIST": "/clients",
            "CREATE": "/clients/create",
            "DELETE": "/clients/delete",
        },
        "BANK_ACCOUNTS": {
            "LIST": "/accounts",
            "CREATE": "/accounts/create",
            "DELETE": "/accounts/delete",
        }
    }
}

class GRAPHQL_QUERIES:
    clients = "static/graphql/query/clients.gql"
    client_bank_accounts = "static/graphql/query/client_bank_accounts.gql"
    bank_accounts = "static/graphql/query/bank_accounts.gql"
    bank_account = "static/graphql/query/bank_account.gql"


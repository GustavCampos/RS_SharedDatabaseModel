import argparse
from cmd import Cmd
import shlex
from filelock import FileLock
from prettytable import PrettyTable
from sqlalchemy.orm import sessionmaker, class_mapper
from database.account import AccountHandler
from database.client import ClientHandler
from database.transaction import TransactionHandler

class AccountManagerCLI(Cmd):
    intro = 'Welcome to the Transaction Manager CLI. Type help or ? to list commands.\n'
    prompt = '(transaction-manager) '
    
    def __init__(self, filelock: FileLock) -> None:
        self.account = AccountHandler(filelock)
        self.client = ClientHandler(filelock)
        self.transaction = TransactionHandler(filelock)
        
        super().__init__()
        
    @staticmethod
    def query_result_to_table(result_obj) -> PrettyTable:
        # Check if query result is not empty
        if not result_obj:
            return "Query result is empty."
        
        table = PrettyTable()
        columns = result_obj.keys()
        table.field_names = columns
        table.add_row([result_obj[col] for col in columns])
        
        return table
    
    @staticmethod
    def query_list_result_to_table(sqlalchemy_list_result) -> PrettyTable:        
        # Check if query result is not empty
        if not sqlalchemy_list_result:
            return "Query result is empty."
        
        # Extract the class of the first entity in the result
        entity_class = type(sqlalchemy_list_result[0])
        
        table = PrettyTable()
        columns = [col.key for col in class_mapper(entity_class).columns]
        
        table.field_names = columns
        
        for entity in sqlalchemy_list_result:
            table.add_row([getattr(entity, col) for col in columns])
            
        return table
    
    def do_get(self, args):
        """
        Get a specific account, client, or transaction by ID.
        Usage: get account <id>
               get client <id>
               get transaction <id>
        """
        parser = argparse.ArgumentParser(prog='get', add_help=False)
        subparsers = parser.add_subparsers(dest='entity', help='Entity to get (account, client, or transaction)')
        
        account_parser = subparsers.add_parser('account')
        account_parser.add_argument('id', type=int, help='ID of the account')
        
        client_parser = subparsers.add_parser('client')
        client_parser.add_argument('id', type=int, help='ID of the client')
        
        transaction_parser = subparsers.add_parser('transaction')
        transaction_parser.add_argument('id', type=int, help='ID of the transaction')
        
        try:
            parsed_args = parser.parse_args(shlex.split(args))
        except SystemExit as e:
            print("Invalid usage. Type 'help get' for details.")
            return e
        
        if parsed_args.entity == "client":
            query_result = self.client.get_client(client_id=parsed_args.id)
            print(AccountManagerCLI.query_result_to_table(query_result))
            
        elif parsed_args.entity == "account":
            query_result = self.account.get_account(account_id=parsed_args.id)
            print(AccountManagerCLI.query_result_to_table(query_result))
        
        elif parsed_args.entity == "transaction":
            query_result = self.transaction.get_transaction(transaction_id=parsed_args.id)
            print(AccountManagerCLI.query_result_to_table(query_result))

    def do_list(self, args):
        """
        List accounts, clients, or transactions with optional filters.
        Usage: list account
               list client
               list transaction
        """
        parser = argparse.ArgumentParser(prog='list', add_help=False)
        subparsers = parser.add_subparsers(dest='entity', help='Entity to list (account, client, or transaction)')
        
        subparsers.add_parser('account')
        subparsers.add_parser('client')
        subparsers.add_parser('transaction')
        
        try:
            parsed_args = parser.parse_args(shlex.split(args))
        except SystemExit as e:
            # Catch argparse help or error and print usage without exiting
            print("Invalid usage. Type 'help list' for details.")
            return e
        
        if parsed_args.entity == "client":
            query_result = self.client.list_client()
            print(AccountManagerCLI.query_list_result_to_table(query_result))
            
        elif parsed_args.entity == "account":
            query_result = self.account.list_account()
            print(AccountManagerCLI.query_list_result_to_table(query_result))
        
        elif parsed_args.entity == "transaction":
            query_result = self.transaction.list_transactions()
            print(AccountManagerCLI.query_list_result_to_table(query_result))
    
    def do_transaction(self, args):
        """
        Create a new transaction.
        Usage: transaction create <transaction_type> [--payer_id <payer_id>] [--receiver_id <receiver_id>] [--password <password>] [--payer_version <payer_version>] [--receiver_version <receiver_version>] <amount>
        """
        parser = argparse.ArgumentParser(prog='transaction', add_help=False)
        subparsers = parser.add_subparsers(dest='action', help='Action to perform (create)')
        
        create_parser = subparsers.add_parser('create')
        create_parser.add_argument('transaction_type', choices=['deposit', 'withdrawal', 'transaction'], help='Type of the transaction')
        create_parser.add_argument('--payer_id', type=int, help='Payer ID for the transaction')
        create_parser.add_argument('--receiver_id', type=int, help='Receiver ID for the transaction')
        create_parser.add_argument('--password', help='Password for the transaction')
        create_parser.add_argument('--payer_version', type=int, help='Payer version for the transaction')
        create_parser.add_argument('--receiver_version', type=int, help='Receiver version for the transaction')
        create_parser.add_argument('amount', type=float, help='Amount for the transaction')
        
        try:
            parsed_args = parser.parse_args(shlex.split(args))
        except SystemExit as e:
            print("Invalid usage. Type 'help transaction' for details.")
            return e
        
        if parsed_args.action == "create":
            new_transaction = self.transaction.create_transaction(
                amount=parsed_args.amount,
                transaction_type=parsed_args.transaction_type,
                payer_id=parsed_args.payer_id,
                receiver_id=parsed_args.receiver_id,
                password=parsed_args.password,
                payer_version=parsed_args.payer_version,
                receiver_version=parsed_args.receiver_version
            )
            print("Transaction created:")
            print(AccountManagerCLI.query_result_to_table(new_transaction))
    
    def do_exit(self, arg):
        'Exit the Account Manager CLI'
        print('Goodbye!')
        return True
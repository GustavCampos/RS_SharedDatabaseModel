import argparse
from cmd import Cmd
import shlex
from filelock import FileLock
from prettytable import PrettyTable
from sqlalchemy.orm import sessionmaker, class_mapper
from database.account import AccountHandler
from database.client import ClientHandler

class AccountManagerCLI(Cmd):
    intro = 'Welcome to the Account Manager CLI. Type help or ? to list commands.\n'
    prompt = '(account-manager) '
    
    def __init__(self, session_maker: sessionmaker, filelock: FileLock) -> None:
        self.account = AccountHandler(session_maker, filelock)
        self.client = ClientHandler(session_maker, filelock)
        
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
        Get a specific account or client by ID.
        Usage: get account <id>
               get client <id>
        """
        parser = argparse.ArgumentParser(prog='get', add_help=False)
        subparsers = parser.add_subparsers(dest='entity', help='Entity to get (account or client)')
        
        account_parser = subparsers.add_parser('account')
        account_parser.add_argument('id', type=int, help='ID of the account')
        
        client_parser = subparsers.add_parser('client')
        client_parser.add_argument('id', type=int, help='ID of the client')
        
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
        

    def do_list(self, args):
        """
        List accounts or clients with optional filters.
        Usage: list account
               list client
        """
        parser = argparse.ArgumentParser(prog='list', add_help=False)
        subparsers = parser.add_subparsers(dest='entity', help='Entity to list (account or client)')
        
        subparsers.add_parser('account')
        subparsers.add_parser('client')
        
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
        

    def do_create(self, args):
        """
        Create a new account or client.
        Usage: create account <owner_id> <password>
               create client <cpf> <complete_name>
        """
        parser = argparse.ArgumentParser(prog='create', add_help=False)
        subparsers = parser.add_subparsers(dest='entity', help='Entity to create (account or client)')
        
        account_parser = subparsers.add_parser('account')
        account_parser.add_argument('owner_id', type=int, help='Owner ID for account')
        account_parser.add_argument('password', help='Password for account')
        
        client_parser = subparsers.add_parser('client')
        client_parser.add_argument('cpf', help='CPF for client')
        client_parser.add_argument('complete_name', help='Complete name for client')
        
        try:
            parsed_args = parser.parse_args(shlex.split(args))
        except SystemExit as e:
            print("Invalid usage. Type 'help create' for details.")
            return e
        
        if parsed_args.entity == "account":
            new_account = self.account.create_account(owner_id=parsed_args.owner_id, password=parsed_args.password)
            print("Account created:")
            print(AccountManagerCLI.query_result_to_table(new_account))
            
        elif parsed_args.entity == "client":
            new_client = self.client.create_client(cpf=parsed_args.cpf, complete_name=parsed_args.complete_name)
            print("Client created:")
            print(AccountManagerCLI.query_result_to_table(new_client))

    def do_update(self, args):
        """
        Update an existing account or client.
        Usage: update account <id> [--owner_id <owner_id>] [--password <password>]
               update client <id> [--cpf <cpf>] [--complete_name <complete_name>]
        """
        parser = argparse.ArgumentParser(prog='update', add_help=False)
        subparsers = parser.add_subparsers(dest='entity', help='Entity to update (account or client)')
        
        account_parser = subparsers.add_parser('account')
        account_parser.add_argument('id', type=int, help='ID of the account')
        account_parser.add_argument('--owner_id', type=int, help='New owner ID for account')
        account_parser.add_argument('--password', help='New password for account')
        
        client_parser = subparsers.add_parser('client')
        client_parser.add_argument('id', type=int, help='ID of the client')
        client_parser.add_argument('--cpf', help='New CPF for client')
        client_parser.add_argument('--complete_name', help='New complete name for client')
        
        try:
            parsed_args = parser.parse_args(shlex.split(args))
        except SystemExit as e:
            print("Invalid usage. Type 'help update' for details.")
            return e
        
        if parsed_args.entity == "account":
            updated_account = self.account.update_account(
                account_id=parsed_args.id,
                owner_id=parsed_args.owner_id,
                password=parsed_args.password
            )
            print("Account updated:")
            print(AccountManagerCLI.query_result_to_table(updated_account))
            
        elif parsed_args.entity == "client":
            updated_client = self.client.update_client(
                client_id=parsed_args.id,
                cpf=parsed_args.cpf,
                complete_name=parsed_args.complete_name
            )
            print("Client updated:")
            print(AccountManagerCLI.query_result_to_table(updated_client))

    def do_delete(self, args):
        """
        Delete an existing account or client.
        Usage: delete account <id>
               delete client <id>
        """
        parser = argparse.ArgumentParser(prog='delete', add_help=False)
        subparsers = parser.add_subparsers(dest='entity', help='Entity to delete (account or client)')
        
        account_parser = subparsers.add_parser('account')
        account_parser.add_argument('id', type=int, help='ID of the account')
        
        client_parser = subparsers.add_parser('client')
        client_parser.add_argument('id', type=int, help='ID of the client')
        
        try:
            parsed_args = parser.parse_args(shlex.split(args))
        except SystemExit as e:
            print("Invalid usage. Type 'help delete' for details.")
            return e
        
        if parsed_args.entity == "account":
            deleted_account = self.account.delete_account(account_id=parsed_args.id)
            print("Account deleted:")
            print(AccountManagerCLI.query_result_to_table(deleted_account))
            
        elif parsed_args.entity == "client":
            deleted_client = self.client.delete_client(client_id=parsed_args.id)
            print("Client deleted:")
            print(AccountManagerCLI.query_result_to_table(deleted_client))
    
    def do_exit(self, arg):
        'Exit the Account Manager CLI'
        print('Goodbye!')
        return True
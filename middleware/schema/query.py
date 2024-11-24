import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from database.table_model import \
    Client as ClientModel, \
    BankAccount as BankAccountModel, \
    Transaction as TransactionModel

class Client(SQLAlchemyObjectType):
    class Meta:
        model = ClientModel
        interfaces = (relay.Node, )

class BankAccount(SQLAlchemyObjectType):
    class Meta:
        model = BankAccountModel
        interfaces = (relay.Node, )

class Transaction(SQLAlchemyObjectType):
    class Meta:
        model = TransactionModel
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    node = relay.Node.Field()

    clients = SQLAlchemyConnectionField(Client.connection)
    accounts = SQLAlchemyConnectionField(BankAccount.connection)
    transactions = SQLAlchemyConnectionField(Transaction.connection)
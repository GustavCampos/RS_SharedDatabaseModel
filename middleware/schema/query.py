import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
import database.table_model as model

class Client(SQLAlchemyObjectType):
    class Meta:
        model = model.Client
        interfaces = (relay.Node, )

class BankAccount(SQLAlchemyObjectType):
    class Meta:
        model = model.BankAccount
        interfaces = (relay.Node, )

class Transaction(SQLAlchemyObjectType):
    class Meta:
        model = model.Transaction
        

class Query(graphene.ObjectType):
    node = relay.Node.Field()

    clients = SQLAlchemyConnectionField(Client.connection)
    accounts = SQLAlchemyConnectionField(BankAccount.connection)
    transactions = SQLAlchemyConnectionField(Transaction.connection)

def GraphQLSchema():
    return graphene.Schema(query=Query)

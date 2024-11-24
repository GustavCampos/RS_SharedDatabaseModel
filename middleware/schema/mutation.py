import graphene
from query import Client, BankAccount, Transaction


class CreateClient(graphene.Mutation):
    class Arguments:
        cpf = graphene.String(required=True)
        complete_name = graphene.String(required=True)        

    client = graphene.Field(Client)
    
    def mutate(self, info, cpf, complete_name):
        db_session = info.context.get('session')
        
        # New Client instance
        
        
class Mutation(graphene.ObjectType):
    create_client = CreateClient.Field()
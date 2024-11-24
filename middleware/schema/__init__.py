import graphene
from query import Query
from mutation import Mutation


def get_graphql_schema():
    return graphene.Schema(query=Query, mutation=Mutation)
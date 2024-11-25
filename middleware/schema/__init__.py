import strawberry
from .query import Query
from .mutation import Mutation


def get_graphql_schema():
    return strawberry.Schema(query=Query, mutation=Mutation)
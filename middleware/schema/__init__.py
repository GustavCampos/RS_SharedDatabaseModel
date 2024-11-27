import strawberry
from strawberry.http.typevars import Context
from flask import Request, Response, g
from strawberry.flask.views import GraphQLView
from strawberry_sqlalchemy_mapper import StrawberrySQLAlchemyLoader
from .model import strawberry_sqlalchemy_mapper, BigInt
from .query import Query
from .mutation import Mutation


def get_graphql_schema():
    strawberry_sqlalchemy_mapper.finalize()
    additional_types = list(strawberry_sqlalchemy_mapper.mapped_types.values())

    return strawberry.Schema(
        query=Query, 
        mutation=Mutation, 
        scalar_overrides={int: BigInt},
        types=additional_types,
    )

class CustomGraphQLView(GraphQLView):
    def get_context(self, request: Request, response: Response) -> Context:
        return {
            **super().get_context(request, response),
            "db_session": g.db_session,
            "sqlalchemy_loader": StrawberrySQLAlchemyLoader(bind=g.db_session),
        }
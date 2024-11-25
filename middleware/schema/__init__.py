from typing import Union
from strawberry.http.typevars import Context
from flask import Request, Response, g
import strawberry
from strawberry.flask.views import GraphQLView
from strawberry_sqlalchemy_mapper import StrawberrySQLAlchemyLoader
from .query import Query, strawberry_sqlalchemy_mapper
from .mutation import Mutation


# BigInt workaround
BigInt = strawberry.scalar(
    Union[int, str],
    serialize=lambda value: int(value),
    parse_value=lambda value: str(value),
    description="BigInt field"
)


def get_graphql_schema():
    strawberry_sqlalchemy_mapper.finalize()
    additional_types = list(strawberry_sqlalchemy_mapper.mapped_types.values())

    return strawberry.Schema(
        query=Query, 
        mutation=Mutation, 
        scalar_overrides={
            int: BigInt
        },
        types=additional_types
    )

class CustomGraphQLView(GraphQLView):
    def get_context(self, request: Request, response: Response) -> Context:
        return {
            **super().get_context(request, response),
            "sqlalchemy_loader": StrawberrySQLAlchemyLoader(bind=g.db_session),
        }
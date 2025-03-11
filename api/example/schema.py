import graphene
from league.schema import Query as LeagueQuery


class Query(LeagueQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)

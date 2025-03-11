import graphene
from league.schema import Query as LeagueQuery
from league.schema import Mutation as LeagueMutation


class Query(LeagueQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=LeagueMutation)

import graphene
from graphene_django import DjangoObjectType
from .models import Team, Player, Match


class TeamType(DjangoObjectType):
    class Meta:
        model = Team
        fields = (
            "uuid",
            "name",
            "players",
            "created_at",
            "updated_at",
            "home_matches",
            "away_matches",
        )


class PlayerType(DjangoObjectType):
    class Meta:
        model = Player
        fields = (
            "uuid",
            "first_name",
            "last_name",
            "jersey_number",
            "team",
            "created_at",
            "updated_at",
        )


class MatchType(DjangoObjectType):
    class Meta:
        model = Match
        fields = (
            "uuid",
            "home_team",
            "away_team",
            "match_date",
            "home_score",
            "away_score",
            "created_at",
            "updated_at",
        )


class Query(graphene.ObjectType):
    # Queries for Teams
    teams = graphene.List(TeamType)
    team = graphene.Field(TeamType, uuid=graphene.UUID())

    # Queries for Players
    players = graphene.List(PlayerType)
    player = graphene.Field(PlayerType, uuid=graphene.UUID())

    # Queries for Matches
    matches = graphene.List(MatchType)
    match = graphene.Field(MatchType, uuid=graphene.UUID())

    def resolve_teams(self, info):
        return Team.objects.all()

    def resolve_team(self, info, uuid):
        return Team.objects.get(uuid=uuid)

    def resolve_players(self, info):
        return Player.objects.all()

    def resolve_player(self, info, uuid):
        return Player.objects.get(uuid=uuid)

    def resolve_matches(self, info):
        return Match.objects.all()

    def resolve_match(self, info, uuid):
        return Match.objects.get(uuid=uuid)


schema = graphene.Schema(query=Query)

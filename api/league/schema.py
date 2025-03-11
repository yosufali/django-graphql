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


# Mutation classes for Team
class CreateTeam(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    team = graphene.Field(TeamType)

    def mutate(self, info, name):
        team = Team.objects.create(name=name)
        return CreateTeam(team=team)


class UpdateTeam(graphene.Mutation):
    class Arguments:
        uuid = graphene.UUID(required=True)
        name = graphene.String(required=True)

    team = graphene.Field(TeamType)

    def mutate(self, info, uuid, name):
        team = Team.objects.get(uuid=uuid)
        team.name = name
        team.save()
        return UpdateTeam(team=team)


class DeleteTeam(graphene.Mutation):
    class Arguments:
        uuid = graphene.UUID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, uuid):
        Team.objects.get(uuid=uuid).delete()
        return DeleteTeam(success=True)


# Mutation classes for Player
class CreatePlayer(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        jersey_number = graphene.Int(required=True)
        team_id = graphene.UUID(required=True)

    player = graphene.Field(PlayerType)

    def mutate(self, info, first_name, last_name, jersey_number, team_id):
        team = Team.objects.get(uuid=team_id)
        player = Player.objects.create(
            first_name=first_name,
            last_name=last_name,
            jersey_number=jersey_number,
            team=team,
        )
        return CreatePlayer(player=player)


class UpdatePlayer(graphene.Mutation):
    class Arguments:
        uuid = graphene.UUID(required=True)
        first_name = graphene.String()
        last_name = graphene.String()
        jersey_number = graphene.Int()
        team_id = graphene.UUID()

    player = graphene.Field(PlayerType)

    def mutate(self, info, uuid, **kwargs):
        player = Player.objects.get(uuid=uuid)

        if "first_name" in kwargs:
            player.first_name = kwargs["first_name"]
        if "last_name" in kwargs:
            player.last_name = kwargs["last_name"]
        if "jersey_number" in kwargs:
            player.jersey_number = kwargs["jersey_number"]
        if "team_id" in kwargs:
            player.team = Team.objects.get(uuid=kwargs["team_id"])

        player.save()
        return UpdatePlayer(player=player)


class DeletePlayer(graphene.Mutation):
    class Arguments:
        uuid = graphene.UUID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, uuid):
        Player.objects.get(uuid=uuid).delete()
        return DeletePlayer(success=True)


# Mutation classes for Match
class CreateMatch(graphene.Mutation):
    class Arguments:
        home_team_id = graphene.UUID(required=True)
        away_team_id = graphene.UUID(required=True)
        match_date = graphene.DateTime(required=True)
        home_score = graphene.Int(required=True)
        away_score = graphene.Int(required=True)

    match = graphene.Field(MatchType)

    def mutate(
        self, info, home_team_id, away_team_id, match_date, home_score, away_score
    ):
        home_team = Team.objects.get(uuid=home_team_id)
        away_team = Team.objects.get(uuid=away_team_id)
        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            match_date=match_date,
            home_score=home_score,
            away_score=away_score,
        )
        return CreateMatch(match=match)


class UpdateMatch(graphene.Mutation):
    class Arguments:
        uuid = graphene.UUID(required=True)
        home_team_id = graphene.UUID()
        away_team_id = graphene.UUID()
        match_date = graphene.DateTime()
        home_score = graphene.Int()
        away_score = graphene.Int()

    match = graphene.Field(MatchType)

    def mutate(self, info, uuid, **kwargs):
        match = Match.objects.get(uuid=uuid)

        if "home_team_id" in kwargs:
            match.home_team = Team.objects.get(uuid=kwargs["home_team_id"])
        if "away_team_id" in kwargs:
            match.away_team = Team.objects.get(uuid=kwargs["away_team_id"])
        if "match_date" in kwargs:
            match.match_date = kwargs["match_date"]
        if "home_score" in kwargs:
            match.home_score = kwargs["home_score"]
        if "away_score" in kwargs:
            match.away_score = kwargs["away_score"]

        match.save()
        return UpdateMatch(match=match)


class DeleteMatch(graphene.Mutation):
    class Arguments:
        uuid = graphene.UUID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, uuid):
        Match.objects.get(uuid=uuid).delete()
        return DeleteMatch(success=True)


class Mutation(graphene.ObjectType):
    create_team = CreateTeam.Field()
    update_team = UpdateTeam.Field()
    delete_team = DeleteTeam.Field()

    create_player = CreatePlayer.Field()
    update_player = UpdatePlayer.Field()
    delete_player = DeletePlayer.Field()

    create_match = CreateMatch.Field()
    update_match = UpdateMatch.Field()
    delete_match = DeleteMatch.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

import uuid
from django.db import models
from django.core.validators import MinValueValidator

class Team(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    jersey_number = models.IntegerField(validators=[MinValueValidator(0)])
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='players',
        null=False,
        blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Match(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    home_team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='home_matches',
        null=False,
        blank=False
    )
    away_team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='away_matches',
        null=False,
        blank=False
    )
    match_date = models.DateTimeField(null=False, blank=False)
    home_score = models.IntegerField(validators=[MinValueValidator(0)], null=False, blank=False)
    away_score = models.IntegerField(validators=[MinValueValidator(0)], null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} - {self.match_date}"

    class Meta:
        verbose_name_plural = 'Matches'

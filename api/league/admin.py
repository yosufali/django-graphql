from django.contrib import admin
from .models import Team, Player, Match

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    readonly_fields = ('uuid', 'created_at', 'updated_at')

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'jersey_number', 'team')
    list_filter = ('team',)
    search_fields = ('first_name', 'last_name')
    readonly_fields = ('uuid', 'created_at', 'updated_at')

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'away_team', 'match_date', 'home_score', 'away_score')
    list_filter = ('match_date', 'home_team', 'away_team')
    search_fields = ('home_team__name', 'away_team__name')
    readonly_fields = ('uuid', 'created_at', 'updated_at')
    date_hierarchy = 'match_date'

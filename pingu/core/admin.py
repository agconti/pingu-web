from django.contrib import admin
from .models import Match, Score, Ranking


class ScoreAdmin(admin.ModelAdmin):
    class Meta:
        model = Score


class MatchAdmin(admin.ModelAdmin):
    class Meta:
        model = Match


class RankingAdmin(admin.ModelAdmin):
    class Meta:
        model = Ranking


admin.site.register(Score, ScoreAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Ranking, RankingAdmin)

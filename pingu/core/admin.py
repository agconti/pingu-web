from django.contrib import admin
from .models import Match, Ranking


class MatchAdmin(admin.ModelAdmin):
    class Meta:
        model = Match


class RankingAdmin(admin.ModelAdmin):
    class Meta:
        model = Ranking


admin.site.register(Match, MatchAdmin)
admin.site.register(Ranking, RankingAdmin)

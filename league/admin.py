from django.contrib import admin
from .models import Season, Team, Field, Game, Player, PlayerGame

admin.site.register(Season)
admin.site.register(Team)
admin.site.register(Field)
admin.site.register(Game)
admin.site.register(Player)
admin.site.register(PlayerGame)
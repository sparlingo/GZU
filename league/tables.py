import django_tables2 as tables
from django_tables2.utils import A
from .models import Game, PlayerStat

class GameTable(tables.Table):
	class Meta:
		model = Game
		sequence = ("hometeam", "awayteam", "field", "game_start", "game_end")
		exclude = ("id", "season", "homescore", "awayscore", "homespirit", "awayspirit", "slug")
		attrs = {"class": "schedule"}
		
class ScoreTable(tables.Table):
	class Meta:
		model = Game
		sequence = ("hometeam", "awayteam", "homescore", "awayscore", "game_start")
		exclude = ("id", "season", "field", "game_end", "homespirit", "awayspirit", "slug")
		attrs = {"class": "scores"}
        
class PlayerStatsTable(tables.Table):
    class Meta:
        model = PlayerStat
        link = tables.LinkColumn('stats_edit', args=[A('id')])
        sequence = ("player", "passes", "catches", "assists", "points", "defences", "drops", "throwaways", )
        exclude = ("team", "game", "multiplier", "id")
        attrs = {"class": "stats"}
from django.contrib import admin
from .models import (Player, Match, Result, MatchEvent, Competition, PlayerStat, ImageControl)

# Register your models here.
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(Result)
admin.site.register(MatchEvent)
admin.site.register(Competition)
admin.site.register(PlayerStat)
admin.site.register(ImageControl)


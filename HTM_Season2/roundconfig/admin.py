from django.contrib import admin
from .models import QuestionSetConfig
from .models import QuestionConfig
from .models import RoundState
from .models import GameState


class RoundStateAdmin(admin.ModelAdmin):
    filter_horizontal = ('allRingers', 'allNSHVers',)


# Register your models here.
admin.site.register(QuestionSetConfig)
admin.site.register(QuestionConfig)
admin.site.register(RoundState, RoundStateAdmin)
admin.site.register(GameState)

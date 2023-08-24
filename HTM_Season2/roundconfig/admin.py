from django.contrib import admin
from .models import QuestionSetConfig
from .models import QuestionConfig
from .models import RoundState

# Register your models here.
admin.site.register(QuestionSetConfig)
admin.site.register(QuestionConfig)
admin.site.register(RoundState)

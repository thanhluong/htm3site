from django.contrib import admin

from .models import ChinhPhucQuestion, ChinhPhucAnswer
from .models import ChinhPhucMap

# Register your models here.
admin.site.register(ChinhPhucQuestion)
admin.site.register(ChinhPhucAnswer)
admin.site.register(ChinhPhucMap)

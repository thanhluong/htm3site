from django.contrib import admin

from .models import ChinhPhucQuestion, ChinhPhucAnswer

# Register your models here.
admin.site.register(ChinhPhucQuestion)
admin.site.register(ChinhPhucAnswer)
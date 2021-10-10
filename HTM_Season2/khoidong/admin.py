from django.contrib import admin
from .models import KhoiDongQuestion, KhoiDongAnswer

# Register your models here.
admin.site.register(KhoiDongQuestion)
admin.site.register(KhoiDongAnswer)
from django.contrib import admin
from .models import MyUser
from .forms import CustomUserCreationForm

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "is_superuser", "is_staff")
    list_filter = ("is_superuser", "is_staff", "is_active")

    fieldsets = [
        ('Thông tin cá nhân', {'fields': ['first_name', 'last_name', 'email']}),
        ('Thông tin đăng nhập', {'fields': ['username', 'password']}),
    ]

# Register your models here.
admin.site.register(MyUser, UserAdmin)

from django.contrib import admin                       # админка
from django.contrib.auth.admin import UserAdmin        # базовая админка User

from .models import User                               # наша модель


@admin.register(User)                                  # регистрируем User
class CustomUserAdmin(UserAdmin):                      # наследуемся от UserAdmin
    list_display = ("username", "full_name", "role", "is_active")  # колонки
    list_filter = ("role", "is_active")                # фильтры справа
    fieldsets = UserAdmin.fieldsets + (                # стандартные секции + наша
        ("Дополнительно", {"fields": ("full_name", "role")}),
    )

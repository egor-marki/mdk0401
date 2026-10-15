from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "get_full_name", "position", "is_active")
    list_filter = ("position", "is_active", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name")

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Дополнительно", {"fields": ("phone", "position")}),
    )

    @admin.display(description="ФИО")
    def get_full_name(self, obj):
        return obj.get_full_name() or "-"

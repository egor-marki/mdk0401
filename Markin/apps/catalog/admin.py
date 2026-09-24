from django.contrib import admin                       # админка

from .models import Category, Location, Model, Vendor  # модели


@admin.register(Location)                              # регистрируем Location
class LocationAdmin(admin.ModelAdmin):                 # свой класс админки
    list_display = ("id", "name")                      # колонки
    search_fields = ("name",)                          # поиск по name


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "vendor", "category")  # 4 колонки
    list_filter = ("vendor", "category")                 # фильтры справа
    search_fields = ("name",)                            # поиск
    autocomplete_fields = ("vendor", "category")         # выпадающий поиск

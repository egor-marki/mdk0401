from django.contrib import admin
from .models import Brand, Car


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "created_at")
    search_fields = ("name",)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "year", "price", "status", "mileage")
    list_filter = ("brand", "status", "fuel_type", "year")
    search_fields = ("model", "vin")
    list_editable = ("status",)

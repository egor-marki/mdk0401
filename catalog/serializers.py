from rest_framework import serializers
from .models import Brand, Car


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "country"]


class CarSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source="brand.name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    fuel_type_display = serializers.CharField(source="get_fuel_type_display", read_only=True)

    class Meta:
        model = Car
        fields = [
            "id", "brand", "brand_name", "model", "year", "price",
            "color", "engine_volume", "fuel_type", "fuel_type_display",
            "transmission", "mileage", "status", "status_display",
            "vin", "description", "created_at",
        ]
        read_only_fields = ["created_at"]

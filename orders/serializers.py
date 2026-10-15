from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source="client.full_name", read_only=True)
    car_name = serializers.CharField(source="car.__str__", read_only=True)
    manager_name = serializers.CharField(source="manager.get_full_name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    order_type_display = serializers.CharField(source="get_order_type_display", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "client", "client_name", "car", "car_name",
            "manager", "manager_name", "order_type", "order_type_display",
            "total_amount", "status", "status_display",
            "comment", "created_at", "completed_at",
        ]
        read_only_fields = ["manager", "created_at", "completed_at"]

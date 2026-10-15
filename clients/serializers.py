from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(
        source="manager.get_full_name", read_only=True,
    )

    class Meta:
        model = Client
        fields = [
            "id", "full_name", "phone", "email",
            "passport", "birth_date", "manager", "manager_name", "created_at",
        ]
        read_only_fields = ["created_at"]

    def validate_phone(self, value):
        """Проверка уникальности телефона."""
        qs = Client.objects.filter(phone=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Клиент с таким телефоном уже есть")
        return value

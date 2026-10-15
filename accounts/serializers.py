from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода данных пользователя."""

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "phone", "position", "is_active"]
        read_only_fields = ["id", "is_active"]


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации."""
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "phone", "position", "password", "password2"]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)  # Хеширование
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """Сериализатор входа."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data["username"],
            password=data["password"],
        )
        if not user:
            raise serializers.ValidationError("Неверный логин или пароль")
        if not user.is_active:
            raise serializers.ValidationError("Аккаунт отключён")
        data["user"] = user
        return data

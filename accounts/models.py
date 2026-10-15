from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомный пользователь с должностью."""

    class Position(models.TextChoices):
        ADMIN = "admin", "Администратор"
        MANAGER = "manager", "Менеджер"
        DIRECTOR = "director", "Директор"

    phone = models.CharField("Телефон", max_length=20, blank=True)
    position = models.CharField(
        "Должность", max_length=20,
        choices=Position.choices, default=Position.MANAGER,
    )

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_position_display()})"

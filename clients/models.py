from django.db import models
from django.conf import settings


class Client(models.Model):
    """Клиент автосалона."""
    full_name = models.CharField("ФИО", max_length=100)
    phone = models.CharField("Телефон", max_length=20, unique=True)
    email = models.EmailField("Email", blank=True)
    passport = models.CharField("Паспорт", max_length=20, blank=True)
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clients",
        verbose_name="Менеджер",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} ({self.phone})"

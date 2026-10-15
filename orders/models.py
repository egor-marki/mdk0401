from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.catalog.models import Car
from apps.clients.models import Client


class Order(models.Model):
    """Заказ: покупка, тест-драйв, сервис."""

    class OrderType(models.TextChoices):
        PURCHASE = "purchase", "Покупка"
        TEST_DRIVE = "test_drive", "Тест-драйв"
        SERVICE = "service", "Сервис"

    class Status(models.TextChoices):
        NEW = "new", "Новый"
        CONFIRMED = "confirmed", "Подтверждён"
        COMPLETED = "completed", "Завершен"
        CANCELLED = "cancelled", "Отменён"

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE,
        related_name="orders", verbose_name="Клиент",
    )
    car = models.ForeignKey(
        Car, on_delete=models.PROTECT,
        related_name="orders", verbose_name="Автомобиль",
    )
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name="orders", verbose_name="Менеджер",
    )
    order_type = models.CharField("Тип", max_length=20, choices=OrderType.choices)
    total_amount = models.DecimalField("Сумма, ₽", max_digits=12, decimal_places=2, default=0)
    status = models.CharField("Статус", max_length=20, choices=Status.choices, default=Status.NEW)
    comment = models.TextField("Комментарий", blank=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    completed_at = models.DateTimeField("Завершен", null=True, blank=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заказ #{self.pk} – {self.client.full_name}"

    def save(self, *args, **kwargs):
        """
        Каскад: при создании purchase – авто резервируется.
        """
        if not self.pk and self.order_type == self.OrderType.PURCHASE:
            if self.car.status == Car.Status.AVAILABLE:
                self.car.status = Car.Status.RESERVED
                self.car.save()
        super().save(*args, **kwargs)

    def complete(self):
        """Завершить заказ с каскадом."""
        self.status = self.Status.COMPLETED
        self.completed_at = timezone.now()
        if self.order_type == self.OrderType.PURCHASE:
            if self.car.status == Car.Status.RESERVED:
                self.car.status = Car.Status.SOLD
                self.car.save()
        self.save()

    def cancel(self):
        """Отменить заказ, вернуть авто в available."""
        self.status = self.Status.CANCELLED
        if self.car.status == Car.Status.RESERVED:
            self.car.status = Car.Status.AVAILABLE
            self.car.save()
        self.save()

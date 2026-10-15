from django.db import models
from django.urls import reverse


class Brand(models.Model):
    """Марка авто."""
    name = models.CharField("Название", max_length=50, unique=True)
    country = models.CharField("Страна", max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Марка"
        verbose_name_plural = "Марки"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Car(models.Model):
    """Автомобиль."""

    class Status(models.TextChoices):
        AVAILABLE = "available", "В наличии"
        RESERVED = "reserved", "Забронирован"
        SOLD = "sold", "Продан"

    class FuelType(models.TextChoices):
        PETROL = "petrol", "Бензин"
        DIESEL = "diesel", "Дизель"
        ELECTRO = "electro", "Электро"
        HYBRID = "hybrid", "Гибрид"

    brand = models.ForeignKey(
        Brand, on_delete=models.PROTECT,
        related_name="cars", verbose_name="Марка",
    )
    model = models.CharField("Модель", max_length=100)
    year = models.PositiveIntegerField("Год")
    price = models.DecimalField("Цена, ₽", max_digits=12, decimal_places=2)
    color = models.CharField("Цвет", max_length=30, blank=True)
    engine_volume = models.DecimalField(
        "Объём, л", max_digits=3, decimal_places=1, null=True, blank=True,
    )
    fuel_type = models.CharField(
        "Топливо", max_length=20, choices=FuelType.choices, blank=True,
    )
    transmission = models.CharField("КПП", max_length=20, blank=True)
    mileage = models.PositiveIntegerField("Пробег, км", default=0)
    status = models.CharField(
        "Статус", max_length=20,
        choices=Status.choices, default=Status.AVAILABLE,
    )
    vin = models.CharField("VIN", max_length=17, unique=True, blank=True, null=True)
    description = models.TextField("Описание", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.brand.name} {self.model} ({self.year})"

    def get_absolute_url(self):
        return reverse("catalog:car_detail", args=[self.pk])

    @property
    def is_available(self):
        return self.status == self.Status.AVAILABLE

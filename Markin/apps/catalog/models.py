from django.db import models                          # поля моделей


class Location(models.Model):                          # модель «Локация»
    name = models.CharField("Название", max_length=255)  # название, до 255 символов

    class Meta:                                        # мета-настройки
        verbose_name = "Локация"                      # имя в ед. числе
        verbose_name_plural = "Локации"               # имя во мн. числе

    def __str__(self):                                # как печатается объект
        return self.name                              # возвращаем название


class Category(models.Model):                          # модель «Категория»
    name = models.CharField("Название", max_length=255)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Vendor(models.Model):                            # модель «Производитель»
    name = models.CharField("Название", max_length=255, unique=True)  # уникальное имя

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"

    def __str__(self):
        return self.name


class Model(models.Model):                             # модель «Модель оборудования»
    vendor = models.ForeignKey(                        # связь с производителем
        Vendor, on_delete=models.PROTECT,             # запрет удаления, если есть ссылки
        verbose_name="Производитель",
    )
    category = models.ForeignKey(                       # связь с категорией
        Category, on_delete=models.PROTECT,
        verbose_name="Категория",
    )
    name = models.CharField("Модель", max_length=255)  # название модели

    class Meta:
        verbose_name = "Модель"
        verbose_name_plural = "Модели"

    def __str__(self):
        return f"{self.vendor.name} {self.name}"       # например, «HP ProBook 450»

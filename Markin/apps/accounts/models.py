from django.contrib.auth.models import AbstractUser  # базовая модель пользователя
from django.db import models                          # поля моделей


class User(AbstractUser):                             # наследуемся от AbstractUser
    class Role(models.TextChoices):                   # перечисление ролей
        ADMIN = "admin", "Администратор"              # код, отображаемое имя
        KEEPER = "keeper", "Кладовщик"
        MOL = "mol", "МОЛ"
        AUDITOR = "auditor", "Аудитор"

    full_name = models.CharField("ФИО", max_length=255, blank=True)  # ФИО, можно пусто
    role = models.CharField(                          # роль
        "Роль", max_length=32,
        choices=Role.choices,                        # ограничить значениями Role
        default=Role.MOL,                            # по умолчанию МОЛ
    )

    def __str__(self):                               # как объект печатается
        return self.full_name or self.username       # ФИО, если пусто — логин

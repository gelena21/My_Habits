from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Модель пользователя, основанная на AbstractUser, с изменениями:
    - Убрано поле username.
    - Добавлено уникальное поле email в качестве основного идентификатора.
    - Добавлено поле chat_id для хранения идентификатора чата.
    """

    username = None

    email = models.EmailField(unique=True, verbose_name="email")
    is_active = models.BooleanField(default=True, verbose_name="активный")
    chat_id = models.CharField(
        max_length=255, verbose_name="номер в чате", blank=True, null=True
    )

    USERNAME_FIELD = (
        "email"  # Устанавливаем email в качестве основного поля для аутентификации
    )
    REQUIRED_FIELDS = []  # Убираем обязательные поля

    def __str__(self):
        """
        Возвращает строковое представление пользователя, состоящее из email и статуса активности.
        """
        return f"{self.email} {self.is_active}"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

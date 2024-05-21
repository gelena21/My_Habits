from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    """
    Команда для создания суперпользователя через консоль.
    """
    def handle(self, *args, **options):
        """
        Основной метод, выполняющий создание суперпользователя.
        """
        user = User.objects.create(
            email='test@admin.ru',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )
        user.set_password('2182')
        user.save()

        self.stdout.write(self.style.SUCCESS(
            "Суперпользователь создан\n"
            "Email: test@admin.ru\n"
            "Пароль: 2182"
        ))

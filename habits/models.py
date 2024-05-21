from django.db import models
from users.models import User


class Habit(models.Model):
    # Пользователь, который создал привычку
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # При удалении пользователя, удаляются и его привычки
        verbose_name='создатель',  # Человекочитаемое имя для отображения в админке
        null=True,
        blank=True,
    )
    # Место, где нужно выполнять привычку
    place = models.CharField(
        max_length=200,
        default='какое-либо место',
        verbose_name='место выполнения'
    )
    # Время выполнения привычки
    time_execute = models.TimeField(
        verbose_name='время на выполнение',
        default='00:00:00'
    )
    # Описание действия, которое нужно выполнить
    action = models.CharField(
        max_length=200,
        verbose_name='действие',
        default='новые действия',
    )
    # Булевое поле, указывающее является ли привычка приятной
    is_nice = models.BooleanField(
        default=False,
        verbose_name='приятность привычки',
    )
    # Связанная привычка (может быть null)
    related_habit = models.ForeignKey(
        'Habit',
        verbose_name='связанная привычка',
        on_delete=models.SET_NULL,  # При удалении связанной привычки, поле станет null
        null=True,
        blank=True,
    )
    # Периодичность выполнения привычки в днях
    periodicity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='периодичность выполнения (в днях)',
    )
    # Вознаграждение за выполнение привычки
    reward = models.CharField(
        max_length=200,
        verbose_name='вознаграждение',
        null=True,
        blank=True,
    )
    # Время на выполнение привычки в секундах
    time_duration = models.PositiveSmallIntegerField(
        verbose_name='время на выполнение в секундах',
        default='60',
    )
    # Булевое поле, указывающее является ли привычка публичной
    is_public = models.BooleanField(
        verbose_name="признак публичности",
        default=True
    )

    def __str__(self):
        # Строковое представление модели для удобного отображения
        return (f'Пользователь: {self.user}\n'
                f'Действие: {self.action}\n'
                f'Время: {self.time_duration}\n'
                f'Место: {self.place}')

    class Meta:
        verbose_name = "привычка",  # Человекочитаемое имя в единственном числе
        verbose_name_plural = "привычки"  # Человекочитаемое имя во множественном числе
        ordering = ("id",)  # Порядок сортировки привычек по id

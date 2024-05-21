from django_celery_beat.models import IntervalSchedule, PeriodicTask
import json
from datetime import datetime, timedelta
from config import settings
import requests

def create_interval(habit):
    """
    Создает интервал и периодическую задачу для привычки.

    :param habit: объект привычки, для которой создается задача
    """
    # Создание или получение интервала с заданной периодичностью (в днях)
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=habit.periodicity,
        period=IntervalSchedule.DAYS,
    )

    # Создание периодической задачи с использованием созданного интервала
    PeriodicTask.objects.create(
        interval=schedule,
        name='Habit',  # Имя задачи
        task='habit.tasks.send_message_habit',  # Полный путь к задаче
        args=json.dumps(['arg1', 'arg2']),  # Аргументы для задачи
        kwargs=json.dumps({
            'be_careful': True,  # Ключевые аргументы для задачи
        }),
        expires=datetime.utcnow() + timedelta(seconds=30)  # Время истечения задачи
    )

def create_bot_telegram(chat_id, text):
    """
    Отправляет сообщение в Telegram чат.

    :param chat_id: ID чата в Telegram, куда будет отправлено сообщение
    :param text: Текст сообщения
    """
    url = 'https://api.telegram.org/bot'  # Базовый URL для Telegram Bot API
    token = settings.TOKEN_BOT_TELEGRAM  # Токен бота, взятый из настроек

    # Отправка POST-запроса для отправки сообщения в Telegram чат
    requests.post(
        url=f'{url}{token}/sendMessage',
        data={
            'chat_id': chat_id,
            'text': text
        }
    )

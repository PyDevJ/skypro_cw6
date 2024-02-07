from django.db import models

from config import settings


class Message(models.Model):
    name = models.CharField(max_length=150, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class Client(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Пользователь',
                             null=True, blank=True)
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    surname = models.CharField(max_length=150, verbose_name='Отчество')
    email = models.EmailField(unique=True, verbose_name='Почта')
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mailings(models.Model):
    stat_mailings = [
        ('start', 'Запущена'),
        ('finish', 'Завершена'),
        ('created', 'Создана')
    ]

    period = [
        ('once_a_day', 'Раз в день'),
        ('once_a_week', 'Раз в неделю'),
        ('once_a_month', 'Раз в месяц')
    ]
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Письмо', blank=True, null=True)
    client = models.ManyToManyField(Client)
    state = models.CharField(max_length=10, choices=stat_mailings, default='start', verbose_name='Статус')
    periodicity = models.CharField(choices=period, default='once_a_day', verbose_name='Переодичность')
    date = models.DateTimeField(verbose_name='время рассылки', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Пользователь',
                             null=True, blank=True)

    def __str__(self):
        return f'{self.state} {self.periodicity}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Log(models.Model):
    stat_mailings = [
        ('start', 'Запущена'),
        ('finish', 'Завершена'),
    ]
    data = models.DateTimeField(verbose_name='дата', null=True, blank=True)
    state = models.CharField(max_length=10, choices=stat_mailings, default='start', verbose_name='Статус')
    email_answer = models.BooleanField(default=False, verbose_name='ответ от почты')

from django.db import models

from config import settings


class Client(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE, verbose_name='Пользователь')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', blank=True, null=True)
    surname = models.CharField(max_length=150, verbose_name='Отчество', blank=True, null=True)
    email = models.EmailField(unique=True, verbose_name='Почта')
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    name = models.CharField(max_length=150, verbose_name='тема письма')
    body = models.TextField(verbose_name='содержимое письма')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='клиент', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return f'{self.state} {self.periodicity}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    permissions = [
        (
            'set_status',
            'Can change status'
        )
    ]


class Log(models.Model):
    stat_mailings = [
        ('start', 'Запущена'),
        ('finish', 'Завершена'),
    ]
    data = models.DateTimeField(verbose_name='дата', null=True, blank=True)
    state = models.CharField(max_length=10, choices=stat_mailings, default='start', verbose_name='статус')
    email_answer = models.BooleanField(default=False, verbose_name='ответ от почты')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE, verbose_name='пользователь')
    mailings = models.ForeignKey('Mailings', on_delete=models.CASCADE, verbose_name='рассылка', null=True, blank=True)

    def __str__(self):
        return f'Отправлено: {self.data} ' \
               f'Статус: {self.state}'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'

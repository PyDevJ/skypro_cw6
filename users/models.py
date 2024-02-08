from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='Почта', unique=True)
    avatar = models.ImageField(upload_to='user/', verbose_name='Аватар', **NULLABLE)
    phone = models.CharField(max_length=25, verbose_name='Номер телефона', **NULLABLE)
    surname = models.CharField(max_length=150, verbose_name='Отчество', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='Активность')
    code = models.CharField(max_length=15, verbose_name='код', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

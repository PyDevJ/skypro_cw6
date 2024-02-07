from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Содержимое', blank=True)
    photo = models.ImageField(upload_to='blog/', verbose_name='Изображение', null=True, blank=True)
    count_views = models.IntegerField(default=0, verbose_name='Просмотров')
    date = models.DateField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return f'{self.title}{self.count_views}{self.body}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

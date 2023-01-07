from django.db import models


class Vacancy(models.Model):
    name = models.TextField(verbose_name='Название')
    key_skills = models.TextField(verbose_name='Навыки')
    salary_from = models.FloatField(verbose_name='Нижняя граница зарплаты')
    salary_to = models.FloatField(verbose_name='Верхняя граница зарплаты')
    salary_currency = models.CharField(max_length=3, verbose_name='Валюта')
    area_name = models.CharField(max_length=50, verbose_name='Город')
    published_at = models.DateTimeField(verbose_name='Дата публикации')

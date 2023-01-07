from django.db import models


class Vacancy(models.Model):
    name = models.TextField(verbose_name='Название')
    key_skills = models.TextField(verbose_name='Навыки')
    salary_from = models.FloatField(verbose_name='Нижняя граница зарплаты')
    salary_to = models.FloatField(verbose_name='Верхняя граница зарплаты')
    salary_currency = models.CharField(max_length=3, verbose_name='Валюта')
    area_name = models.CharField(max_length=50, verbose_name='Город')
    published_at = models.DateTimeField(verbose_name='Дата публикации')


class Demand(models.Model):
    year = models.SmallIntegerField(primary_key=True, verbose_name='Год')
    salary = models.IntegerField(verbose_name='Зарплата в рублях')
    count = models.IntegerField(verbose_name='Количество вакансий')
    chosen_salary = models.IntegerField(verbose_name='Зарплата в рублях для выбранной профессии')
    chosen_count = models.IntegerField(verbose_name='Количество вакансий для выбранной профессии')


class Geography(models.Model):
    area_name = models.CharField(primary_key=True, max_length=50, verbose_name='Город')
    salary = models.IntegerField(verbose_name='Зарплата в рублях')
    fraction = models.DecimalField(verbose_name='Доля вакансий', max_digits=4, decimal_places=3)


class Skills(models.Model):
    skill = models.CharField(max_length=100, verbose_name='Навык')
    count = models.IntegerField(verbose_name='Количество вакансий')

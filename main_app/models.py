from django.db import models



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


class Year(models.Model):
    year = models.SmallIntegerField(primary_key=True, verbose_name='Год')


class Skill(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    skill = models.CharField(max_length=100, verbose_name='Навык')
    count = models.IntegerField(verbose_name='Количество вакансий')

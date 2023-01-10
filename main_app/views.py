from django.shortcuts import render
from .models import Demand, Geography
from pathlib import Path
import csv


def csv_to_db_for_demand(model, path_to_csv):
    with open(path_to_csv, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            obj = model()
            obj.year = int(row['Year'])
            obj.count = int(float(row['count_vacancies'])) if row['count_vacancies'] != '' else 0
            obj.salary = int(float(row['avg_salary'])) if row['avg_salary'] != '' else 0
            obj.chosen_salary = int(float(row['avg_salary_for_selected'])) if row['avg_salary_for_selected'] != '' else 0
            obj.chosen_count = int(float(row['count_vacancies_for_selected'])) if row['count_vacancies_for_selected'] != '' else 0
            obj.save()

def csv_to_db_for_geography(model, path_to_csv):
    with open(path_to_csv, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            obj = model()
            obj.area_name = row['area_name']
            obj.fraction = float(row['fraction_vacancies']) if row['fraction_vacancies'] != '' else 0
            obj.salary = int(float(row['avg_salary'])) if row['avg_salary'] != '' else 0
            obj.save()

def index(request):
    return render(request, 'index.html')


def geography(request):
    salary = Geography.objects.order_by('-salary').values()
    fraction = Geography.objects.order_by('-fraction').values()
    path = Path(__file__).parent / r'static\tables\geography'
    if len(salary) == 0 or len(fraction) == 0:
        csv_to_db_for_geography(Geography, path / r'compile.csv')
        salary = Geography.objects.order_by('-salary').values()
        fraction = Geography.objects.order_by('-fraction').values()
    return render(request, 'geography.html', context={'salary': salary, 'fraction': fraction})


def demand(request):
    statistics = Demand.objects.values()
    path = Path(__file__).parent / r'static\tables\demand'
    if len(statistics) == 0:
        csv_to_db_for_demand(Demand, path / r'compile.csv')
        statistics = Demand.objects.values()
    return render(request, 'demand.html', context={'statistics': statistics})


def last_vacancies(request):
    return render(request, 'last_vacancies.html')


def skills(request):
    return render(request, 'skills.html')

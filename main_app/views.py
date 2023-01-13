from datetime import timedelta, datetime
import re
from functools import reduce

from django.http import HttpResponse, Http404
from django.shortcuts import render
from .models import Demand, Geography, Skill, Year, Vacancy
from pathlib import Path
import csv
import requests
import json, time


def csv_to_db_for_demand(model, path_to_csv):
    with open(path_to_csv, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            obj = model()
            obj.year = int(row['Year'])
            obj.count = int(float(row['count_vacancies'])) if row['count_vacancies'] != '' else 0
            obj.salary = int(float(row['avg_salary'])) if row['avg_salary'] != '' else 0
            obj.chosen_salary = int(float(row['avg_salary_for_selected'])) if row[
                                                                                  'avg_salary_for_selected'] != '' else 0
            obj.chosen_count = int(float(row['count_vacancies_for_selected'])) if row[
                                                                                      'count_vacancies_for_selected'] != '' else 0
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


def csv_to_db_for_skills(path_to_csv):
    with open(path_to_csv, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            year, created = Year.objects.get_or_create(year=int(row['year']))
            obj = Skill()
            obj.rank = int(row['rank'])
            obj.skill = row['skill']
            obj.count = int(row['count_skill'])
            year.skill_set.add(obj, bulk=False)


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
    if len(statistics) == 0:
        path = Path(__file__).parent / r'static\tables\demand'
        csv_to_db_for_demand(Demand, path / r'compile.csv')
        statistics = Demand.objects.values()
    return render(request, 'demand.html', context={'statistics': statistics})


def get_wrap(url, params):
    req = requests.get(url, params)
    data = req.content.decode()
    try:
        if req.status_code == 200:
            return data, 200
        if req.status_code == 403:
            return data, 403
        else:
            return None, req.status_code
    finally:
        req.close()


def clear(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r' +', ' ', s).strip()
    return s

def to_db(vac):
    obj = Vacancy()
    try:
        obj.name = vac['name']
        if vac['salary'] != None:
            obj.salary = (vac['salary']['from'] + vac['salary']['to']) // 2
            obj.salary_currency = vac['salary']['currency']
        if vac['area'] != None:
            obj.area_name = vac['area']['name']
        if vac['key_skills'] != None:
            res = ''
            for skill in vac['key_skills']:
                res += skill['name'] + ', '
            obj.skills = res[:-2]
        if vac['employer'] != None:
            obj.company = vac['employer']['name']
        obj.published_at = datetime.fromisoformat(vac['published_at'])
        obj.description = clear(vac['description'])
        obj.href = vac['alternate_url']
        obj.save()
    except:
        return HttpResponse(vac)


def vacancies_to_db(idies):
    for id in idies:
        vacancy = json.loads(get_wrap(f'https://api.hh.ru/vacancies/{id}', {})[0])
        to_db(vacancy)


def get_idies(jsn):
    idies = []
    for d in jsn['items']:
        idies.append(d['id'])
    return idies


def last_vacancies(request):
    now = datetime.now()
    delta = now - timedelta(29)

    params = {
        'text': 'ios',
        'search_field': 'name',
        'specialization': 1,
        'date_from': f'{delta.year}-{delta.month}-{delta.day}T00:00:00+0300',
    }
    data, code = get_wrap('https://api.hh.ru/vacancies', params)
    if code == 403:
        return HttpResponse(json.loads(data['captcha_url']))
    elif code != 200:
        return render(request, 'error.html', context={'code': code, 'text': f'Возникла ошибка({code})!'})
    Vacancy.objects.all().delete()
    idies = get_idies(json.loads(data))
    vacancies_to_db(idies)
    vacancies = Vacancy.objects.order_by('-published_at').values()
    return render(request, 'last_vacancies.html', context={'vacancies': vacancies})


def group_by(big_d, key):
    res = {}
    for d in big_d:
        if d[key] not in res:
            res[d[key]] = []
        res[d[key]].append({})
        for k in d:
            if k != key:
                res[d[key]][-1][k] = d[k]
    return res


def skills(request):
    skills = Skill.objects.values("year_id", "rank", "skill", "count")
    if len(skills) == 0:
        path = Path(__file__).parent / r'static\tables\skills'
        csv_to_db_for_skills(path / 'compile.csv')
        skills = Skill.objects.values()
    skills = group_by(skills, 'year_id')
    return render(request, 'skills.html', context={'skills': skills, 'reverse': reversed})

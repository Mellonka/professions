from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def index(request):
    return render(request, 'index.html')


def geography(request):
    return render(request, 'geography.html')


def demand(request):
    return render(request, 'demand.html')


def last_vacancies(request):
    return render(request, 'last_vacancies.html')


def skills(request):
    return render(request, 'skills.html')

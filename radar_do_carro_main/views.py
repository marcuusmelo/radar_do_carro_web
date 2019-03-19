from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django_tables2 import RequestConfig

from radar_do_carro_main.models import CarAdTest
from radar_do_carro_main.tables import CarAdTestTable


def dashboard(request):
    """
    Experiment -- this will eventually be the table page for radar do carro
    Objectives:
        1. [Y] Display a db table
        2. [Y] Front end sort
        3. [ ] Front end filter
        4. [Y] Make it look pretty
    """
    table = CarAdTestTable(CarAdTest.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'radar_do_carro_main/tables.html', {'table': table})

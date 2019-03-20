from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django_tables2 import RequestConfig

from radar_do_carro_main.models import CarAdTest
from radar_do_carro_main.tables import CarAdTestTable

from .filters import CarAdTestFilter

"""from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin


class FilteredCarAdTest(SingleTableMixin, FilterView):
    table_class = CarAdTestTable
    model = CarAdTest
    template_name = 'radar_do_carro_main/tables.html'

    filterset_class = CarAdTestFilter"""

def dashboard(request, page_type='todos'):
    """Experiment -- this will eventually be the table page for radar do carro
    Objectives:
        1. [Y] Display a db table
        2. [Y] Front end sort
        3. [Y] Front end filter
        4. [Y] Make it look pretty
        5. [ ] Put real data in"""
    car_ads_qs = CarAdTest.objects.all()

    if page_type == 'mais_vendidos':
        pass
    elif page_type == 'seda_compacto':
        pass
    elif page_type == 'seda_medio':
        pass
    elif page_type == 'suv':
        pass

    if "modelo" in request.GET:
        modelo = request.GET["modelo"]
        if modelo != '':
            car_ads_qs = car_ads_qs.filter(modelo__exact=modelo)

    if "ano_min" in request.GET:
        ano_min = request.GET["ano_min"]
        if ano_min != '':
            car_ads_qs = car_ads_qs.filter(ano__gte=ano_min)

    if "ano_max" in request.GET:
        ano_max = request.GET["ano_max"]
        if ano_max != '':
            car_ads_qs = car_ads_qs.filter(ano__lte=ano_max)

    if "preco_min" in request.GET:
        preco_min = request.GET["preco_min"]
        if preco_min != '':
            car_ads_qs = car_ads_qs.filter(preco__gte=preco_min)

    if "preco_max" in request.GET:
        preco_max = request.GET["preco_max"]
        if preco_max != '':
            car_ads_qs = car_ads_qs.filter(preco__lte=preco_max)

    if "km_min" in request.GET:
        km_min = request.GET["km_min"]
        if km_min != '':
            car_ads_qs = car_ads_qs.filter(km_odometro__gte=km_min)

    if "km_max" in request.GET:
        km_max = request.GET["km_max"]
        if km_max != '':
            car_ads_qs = car_ads_qs.filter(km_odometro__lte=km_max)


    table = CarAdTestTable(car_ads_qs)
    RequestConfig(request).configure(table)

    page_type = page_type.replace('_', ' ').replace('seda', 'SEDÃ').upper()

    return render(request, 'radar_do_carro_main/tables.html', {'table': table, 'page': page_type})

    #f = CarAdTestFilter(request.GET, queryset=CarAdTest.objects.all())
    #return render(request, 'radar_do_carro_main/tables.html', {'table': f})

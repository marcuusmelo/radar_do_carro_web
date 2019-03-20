from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django_tables2 import RequestConfig

from radar_do_carro_main.models import CarAdTest
from radar_do_carro_main.tables import CarAdTestTable

from .filters import CarAdTestFilter


def dashboard(request, marca_modelo='todos'):
    """  """
    modelos_disponiveis = [
        'todos', 'mais_vendidos', 'seda_compacto', 'seda_medio', 'suv', 'hb20', 'onix',
        'gol', 'up', 'kwid', 'ka', 'prisma', 'virtus', 'ka_seda', 'voyage'
    ]

    if marca_modelo not in modelos_disponiveis:
        return render(request, 'radar_do_carro_main/404.html')

    car_ads_qs = CarAdTest.objects.all()

    if marca_modelo == 'todos':
        pass
    elif marca_modelo == 'mais_vendidos':
        pass
    elif marca_modelo == 'seda_compacto':
        pass
    elif marca_modelo == 'seda_medio':
        pass
    elif marca_modelo == 'suv':
        pass
    else:
        pass

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

    marca_modelo = marca_modelo.replace('_', ' ').replace('seda', 'SEDÃ').upper()

    args = {
        'table': table,
        'page': marca_modelo
    }

    return render(request, 'radar_do_carro_main/tables.html', args)

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django_tables2 import RequestConfig
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth import logout

import bson

from .forms import RegistrationForm
from radar_do_carro_main.models import CarAdTest, FipeFinal, CarAdData
from radar_do_carro_main.tables import CarAdTestTable, FipeFinalTable, CarAdDataTable
from .filters import CarAdTestFilter


def index(request):
    """ Home page render """
    return render(request, 'radar_do_carro_main/index.html')


def criar_conta(request):
    """ Register new user accounts """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Radar do Carro - Ative sua Conta'
            message = render_to_string('radar_do_carro_main/email_ativacao.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'radar_do_carro_main/aguardando_ativacao.html')
    else:
        form = RegistrationForm()

    args = {'form': form}
    return render(request, 'radar_do_carro_main/criar_conta.html', args)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        activation_status = True
    else:
        activation_status = False

    args = {'activated': activation_status}
    return render(request, 'radar_do_carro_main/conta_ativada_planos.html', args)


def go_to_ad(request, ad_id):
    car_ads_qs = CarAdData.objects.all()
    car_ads_list = [x for x in car_ads_qs if x._id == bson.objectid.ObjectId(ad_id)]
    url_to_redirect = car_ads_list[0].ad_link
    return redirect(url_to_redirect)


@login_required(login_url='/login/')
def logout_view(request):
    """ Logout the user """
    logout(request)
    return redirect('index')


# Add a decorator for permission required as well
# from django.contrib.auth.decorators import permission_required
# @permission_required('radar_do_carro_main.assinatura_valida')
@login_required(login_url='/login/')
def dashboard(request, marca_modelo='todos'):
    """ Fetch, filter and sort table to be displayed in the dashboard """
    categorias_disponiveis = [
        'todos', 'mais_vendidos', 'seda_compacto', 'seda_medio', 'suv'
    ]

    modelos_disponiveis = [
        'cobalt', 'cruze_sedan', 'onix', 'prisma', 's10', 'spin', 'tracker', 'argo', 'cronos',
        'mobi', 'siena', 'strada', 'toro', 'uno', 'ecosport', 'fiesta', 'focus', 'fusion', 'ka',
        'ka_sedan', 'ranger', 'city', 'civic', 'fit', 'hr-v', 'wr-v', 'creta', 'hb20', 'hb20s',
        'compass', 'renegade', 'kicks', 'sentra', 'versa', 'captur', 'duster', 'kwid', 'logan',
        'sandero', 'corolla', 'etios_hatch', 'etios_sedan', 'hilux', 'yaris_hatch', 'yaris_sedan',
        'amarok', 'fox', 'gol', 'golf', 'jetta', 'polo', 'saveiro', 'up', 'virtus', 'voyage'
    ]

    mais_vendidos = ['onix', 'hb20', 'ka', 'gol', 'kwid']

    seda_compacto = ['prisma', 'virtus', 'ka_sedan', 'voyage', 'hb20s']

    seda_medio = ['corolla', 'civic', 'cruze_sedan', 'sentra', 'jetta']

    suv = ['compass', 'creta', 'hr-v', 'kicks', 'renegade']

    if marca_modelo not in modelos_disponiveis+categorias_disponiveis:
        return render(request, 'radar_do_carro_main/404.html')

    car_ads_qs = CarAdData.objects.order_by('-car_year', '-ad_date')#.order_by('-ad_date')

    if marca_modelo == 'todos':
        pass
    elif marca_modelo == 'mais_vendidos':
        mais_vendidos = [x.upper() for x in mais_vendidos]
        car_ads_qs = car_ads_qs.filter(car_model_code__in=mais_vendidos)
    elif marca_modelo == 'seda_compacto':
        seda_compacto = [x.upper() for x in seda_compacto]
        car_ads_qs = car_ads_qs.filter(car_model_code__in=seda_compacto)
    elif marca_modelo == 'seda_medio':
        seda_medio = [x.upper() for x in seda_medio]
        car_ads_qs = car_ads_qs.filter(car_model_code__in=seda_medio)
    elif marca_modelo == 'suv':
        suv = [x.upper() for x in suv]
        car_ads_qs = car_ads_qs.filter(car_model_code__in=suv)
    else:
        marca_modelo = marca_modelo.upper()
        car_ads_qs = car_ads_qs.filter(car_model_code__exact=marca_modelo)

    if "ano_min" in request.GET:
        ano_min = request.GET["ano_min"]
        if ano_min != '':
            car_ads_qs = [x for x in car_ads_qs if x.car_km >= int(ano_min)]

    if "ano_max" in request.GET:
        ano_max = request.GET["ano_max"]
        if ano_max != '':
            car_ads_qs = [x for x in car_ads_qs if x.car_km <= int(ano_max)]

    if "preco_min" in request.GET:
        preco_min = request.GET["preco_min"]
        if preco_min != '':
            car_ads_qs = [x for x in car_ads_qs if x.car_km >= int(preco_min)]

    if "preco_max" in request.GET:
        preco_max = request.GET["preco_max"]
        if preco_max != '':
            car_ads_qs = [x for x in car_ads_qs if x.car_km <= int(preco_max)]

    if "km_min" in request.GET:
        km_min = request.GET["km_min"]
        if km_min != '':
            car_ads_qs = [x for x in car_ads_qs if x.car_km >= int(km_min)]

    if "km_max" in request.GET:
        km_max = request.GET["km_max"]
        if km_max != '':
            car_ads_qs = [x for x in car_ads_qs if x.car_km <= int(km_max)]

    number_of_entries = len(car_ads_qs)
    table = CarAdDataTable(car_ads_qs)
    RequestConfig(request).configure(table)

    marca_modelo = marca_modelo.replace('_', ' ').replace('seda', 'SEDÃ').upper()

    args = {
        'table': table,
        'page': marca_modelo + ' - ' + str(number_of_entries) + ' resultados'
    }

    return render(request, 'radar_do_carro_main/tables_dashboard.html', args)


# Add a decorator for permission required as well
# from django.contrib.auth.decorators import permission_required
# @permission_required('radar_do_carro_main.assinatura_valida')
#@login_required(login_url='/login/')
def fipe(request, marca_modelo='todos'):
    """ Fetch, filter and sort table to be displayed in the dashboard """
    categorias_disponiveis = [
        'todos', 'mais_vendidos', 'seda_compacto', 'seda_medio', 'suv'
    ]

    modelos_disponiveis = [
        'cobalt', 'cruze_sedan', 'onix', 'prisma', 's10', 'spin', 'tracker', 'argo', 'cronos',
        'mobi', 'siena', 'strada', 'toro', 'uno', 'ecosport', 'fiesta', 'focus', 'fusion', 'ka',
        'ka_sedan', 'ranger', 'city', 'civic', 'fit', 'hr-v', 'wr-v', 'creta', 'hb20', 'hb20s',
        'compass', 'renegade', 'kicks', 'sentra', 'versa', 'captur', 'duster', 'kwid', 'logan',
        'sandero', 'corolla', 'etios_hatch', 'etios_sedan', 'hilux', 'yaris_hatch', 'yaris_sedan',
        'amarok', 'fox', 'gol', 'golf', 'jetta', 'polo', 'saveiro', 'up', 'virtus', 'voyage'
    ]

    mais_vendidos = ['onix', 'hb20', 'ka', 'gol', 'kwid']

    seda_compacto = ['prisma', 'virtus', 'ka_sedan', 'voyage', 'hb20s']

    seda_medio = ['corolla', 'civic', 'cruze_sedan', 'sentra', 'jetta']

    suv = ['compass', 'creta', 'hr-v', 'kicks', 'renegade']

    if marca_modelo not in modelos_disponiveis+categorias_disponiveis:
        return render(request, 'radar_do_carro_main/404.html')

    car_ads_qs = FipeFinal.objects.all()

    if marca_modelo == 'todos':
        pass
    else:
        car_ads_qs = car_ads_qs.filter(modelo_code__exact=marca_modelo.upper())

    if "ano" in request.GET:
        ano = request.GET["ano"].replace('+', ' ')
        if ano != '':
            car_ads_qs = [x for x in car_ads_qs if x.ano == ano]

    if "pot" in request.GET:
        potencia = request.GET["pot"]
        if potencia != '':
            car_ads_qs = [x for x in car_ads_qs if x.potencia == float(potencia)]

    if "transm" in request.GET:
        transmissao = request.GET["transm"]
        if transmissao != '':
            car_ads_qs = [x for x in car_ads_qs if x.transm == transmissao]

    number_of_entries = len(car_ads_qs)
    table = FipeFinalTable(car_ads_qs)
    RequestConfig(request).configure(table)

    marca_modelo = marca_modelo.replace('_', ' ').replace('seda', 'SEDÃ').upper()

    args = {
        'table': table,
        'page': marca_modelo + ' - ' + str(number_of_entries) + ' resultados'
    }

    return render(request, 'radar_do_carro_main/tables_fipe.html', args)

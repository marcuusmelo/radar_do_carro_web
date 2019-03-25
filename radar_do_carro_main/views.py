from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django_tables2 import RequestConfig
from django.contrib.auth.decorators import login_required, permission_required

from .forms import RegistrationForm

from radar_do_carro_main.models import CarAdTest
from radar_do_carro_main.tables import CarAdTestTable

from django.contrib.auth import logout

from .filters import CarAdTestFilter


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

    car_ads_qs = CarAdTest.objects.all()

    if marca_modelo == 'todos':
        pass
    elif marca_modelo == 'mais_vendidos':
        car_ads_qs = car_ads_qs.filter(modelo__in=mais_vendidos)
    elif marca_modelo == 'seda_compacto':
        car_ads_qs = car_ads_qs.filter(modelo__in=seda_compacto)
    elif marca_modelo == 'seda_medio':
        car_ads_qs = car_ads_qs.filter(modelo__in=seda_medio)
    elif marca_modelo == 'suv':
        car_ads_qs = car_ads_qs.filter(modelo__in=suv)
    else:
        car_ads_qs = car_ads_qs.filter(modelo__exact=marca_modelo)

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

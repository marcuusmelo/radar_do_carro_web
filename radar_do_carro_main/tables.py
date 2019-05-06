import django_tables2 as tables
from django_tables2.utils import A
from .models import *

class CarAdTestTable(tables.Table):
    class Meta:
        model=CarAdTest
        template_name = 'django_tables2/bootstrap.html'


class CarAdDataTable(tables.Table):
    ad_link = tables.columns.LinkColumn('go_to_ad', text='Anúncio', args=[A('pk')])
    class Meta:
        model=CarAdData

        fields = ('car_brand', 'car_model_code', 'car_model_name', 'car_year', 'car_km',
                  'car_power', 'car_transmission', 'car_price', 'fipe_price_exact',
                  'fipe_price_min', 'fipe_price_max', 'phone_number', 'ad_date', 'ad_link')
        template_name = 'django_tables2/bootstrap.html'


class FipeFinalTable(tables.Table):
    class Meta:
        model=FipeFinal
        fields = ('marca', 'modelo_code', 'modelo_nome', 'ano', 'potencia', 'transm', 'preco')
        template_name = 'django_tables2/bootstrap.html'

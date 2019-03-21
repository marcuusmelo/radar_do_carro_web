import django_filters
from.models import CarAdTest


class CarAdTestFilter(django_filters.FilterSet):

    class Meta:
        model = CarAdTest
        fields = {
            'marca': ['exact'],
            'modelo': ['exact'],
            'motor': ['lt', 'gt'],
            'ano': ['lt', 'gt'],
            'preco': ['lt', 'gt'],
            'km_odometro': ['lt', 'gt']
        }

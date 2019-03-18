import django_tables2 as tables
from .models import CarAdTest

class CarAdTestTable(tables.Table):
    class Meta:
        model=CarAdTest
        template_name = 'django_tables2/bootstrap.html'

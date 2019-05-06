from django.db import models


class CarAdTest(models.Model):
    marca = models.CharField(max_length=200)
    modelo = models.CharField(max_length=200)
    motor = models.CharField(max_length=200)
    ano = models.IntegerField()
    preco = models.FloatField()
    fipe = models.FloatField()
    km_odometro = models.FloatField()


class FipeFinal(models.Model):
    _id = models.CharField(max_length=200, primary_key=True, default="")
    marca = models.CharField('MARCA', max_length=200)
    modelo_code = models.CharField('MODELO.', max_length=200)
    modelo_nome = models.CharField('MODELO COMP.', max_length=200)
    ano = models.CharField('ANO', max_length=200)
    potencia = models.CharField('POTÊNCIA', max_length=200)
    transm = models.CharField('TRANSMISSÃO', max_length=200)
    preco = models.CharField('PREÇO', max_length=200)
    data_processamento = models.CharField('DATA PROC', max_length=200)


class CarAdData(models.Model):
    _id = models.CharField(max_length=200, primary_key=True, default="")
    car_brand = models.CharField('MARCA', max_length=200)
    car_model_code = models.CharField('MODELO', max_length=200)
    car_model_name = models.CharField('MODELO COMPL.', max_length=200)
    car_year = models.CharField('ANO', max_length=200)
    car_km = models.CharField('KM', max_length=200)
    car_power = models.CharField('P.', max_length=200)
    car_transmission = models.CharField('T.', max_length=200)
    car_price = models.CharField('PREÇO', max_length=200)
    fipe_price_exact = models.CharField('FIPE', max_length=200)
    fipe_price_min = models.CharField('FIPEMIN', max_length=200)
    fipe_price_max = models.CharField('FIPEMAX', max_length=200)
    phone_number = models.CharField('CONTATO', max_length=200)
    ad_date = models.CharField('DATA', max_length=200)
    ad_id = models.CharField('ID', max_length=200)
    ad_link = models.URLField('LINKS')
    fetch_datetime = models.CharField('DATA VIZ.', max_length=200)

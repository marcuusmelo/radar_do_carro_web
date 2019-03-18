from django.db import models


class CarAdTest(models.Model):
    marca = models.CharField(max_length=200)
    modelo = models.CharField(max_length=200)
    motor = models.CharField(max_length=200)
    ano = models.IntegerField()
    preco = models.FloatField()
    fipe = models.FloatField()
    km_odometro = models.FloatField()

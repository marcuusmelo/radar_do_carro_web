# Generated by Django 2.1.7 on 2019-05-02 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('radar_do_carro_main', '0003_auto_20190502_2316'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarAdData',
            fields=[
                ('_id', models.CharField(default='', max_length=200, primary_key=True, serialize=False)),
                ('car_brand', models.CharField(max_length=200)),
                ('car_model_code', models.CharField(max_length=200)),
                ('car_model_name', models.CharField(max_length=200)),
                ('car_year', models.CharField(max_length=200)),
                ('car_km', models.CharField(max_length=200)),
                ('car_power', models.CharField(max_length=200)),
                ('car_transmission', models.CharField(max_length=200)),
                ('car_price', models.CharField(max_length=200)),
                ('fipe_price_exact', models.CharField(max_length=200)),
                ('fipe_price_min', models.CharField(max_length=200)),
                ('fipe_price_max', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=200)),
                ('ad_date', models.CharField(max_length=200)),
                ('ad_id', models.CharField(max_length=200)),
                ('ad_link', models.CharField(max_length=200)),
                ('fetch_datetime', models.CharField(max_length=200)),
            ],
        ),
    ]

# Generated by Django 2.1.7 on 2019-03-16 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarAdTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca', models.CharField(max_length=200)),
                ('modelo', models.CharField(max_length=200)),
                ('motor', models.CharField(max_length=200)),
                ('ano', models.IntegerField()),
                ('preco', models.FloatField()),
                ('fipe', models.FloatField()),
                ('km_odometro', models.FloatField()),
            ],
        ),
    ]

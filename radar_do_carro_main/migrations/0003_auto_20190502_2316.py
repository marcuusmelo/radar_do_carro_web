# Generated by Django 2.1.7 on 2019-05-02 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('radar_do_carro_main', '0002_fipefinal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fipefinal',
            name='id',
        ),
        migrations.AddField(
            model_name='fipefinal',
            name='_id',
            field=models.CharField(default='', max_length=200, primary_key=True, serialize=False),
        ),
    ]

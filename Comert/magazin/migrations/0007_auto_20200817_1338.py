# Generated by Django 3.1 on 2020-08-17 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('magazin', '0006_auto_20200817_0052'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comanda',
            options={'ordering': ['-creata'], 'verbose_name': 'Comanda', 'verbose_name_plural': 'Comenzi'},
        ),
    ]

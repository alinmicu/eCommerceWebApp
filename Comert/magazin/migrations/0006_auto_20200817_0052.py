# Generated by Django 3.1 on 2020-08-16 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magazin', '0005_comanda_tarafacturare'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comanda',
            name='adresa_email',
            field=models.EmailField(blank=True, max_length=250, verbose_name='Adresa de email'),
        ),
        migrations.AlterField(
            model_name='comanda',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total comanda'),
        ),
    ]

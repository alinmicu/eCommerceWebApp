# Generated by Django 3.1 on 2020-08-15 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('magazin', '0002_auto_20200815_1644'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_cos', models.CharField(blank=True, max_length=250)),
                ('data_adaugarii', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Cos',
                'ordering': ['data_adaugarii'],
            },
        ),
        migrations.CreateModel(
            name='ObiectCos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantitate', models.IntegerField()),
                ('stare_activa', models.BooleanField(default=True)),
                ('cos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magazin.cos')),
                ('produs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magazin.produs')),
            ],
            options={
                'db_table': 'ObiectCos',
            },
        ),
    ]
# Generated by Django 5.0.3 on 2024-05-02 10:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CuisineCountry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('flag', models.ImageField(blank=True, null=True, upload_to='flags/')),
                ('code', models.CharField(blank=True, max_length=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='cuisines/')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cuisines', to='recipes.cuisinecountry')),
            ],
        ),
    ]

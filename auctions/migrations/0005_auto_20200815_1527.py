# Generated by Django 3.0.8 on 2020-08-15 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auctions_listed_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='price',
            field=models.FloatField(),
        ),
    ]

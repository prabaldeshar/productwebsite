# Generated by Django 2.2.2 on 2019-06-24 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='rating',
            field=models.IntegerField(blank=True),
        ),
    ]

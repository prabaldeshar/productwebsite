# Generated by Django 2.2.2 on 2019-07-31 05:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_comment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]

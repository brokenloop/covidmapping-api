# Generated by Django 3.0.4 on 2020-03-13 23:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0007_auto_20200313_1736'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='coronacaseraw',
            name='location',
        ),
    ]

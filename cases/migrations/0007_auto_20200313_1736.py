# Generated by Django 3.0.4 on 2020-03-13 21:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0006_auto_20200312_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='coronacaseraw',
            name='date_received',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='coronacaseraw',
            name='update_flag',
            field=models.BooleanField(default=False),
        ),
    ]
# Generated by Django 3.0.4 on 2020-03-12 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0002_auto_20200312_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='coronacaseraw',
            name='name',
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
    ]

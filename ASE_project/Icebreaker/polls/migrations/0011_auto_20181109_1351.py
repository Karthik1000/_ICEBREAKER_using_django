# Generated by Django 2.1.1 on 2018-11-09 08:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_auto_20181109_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 11, 9, 8, 21, 25, 429085, tzinfo=utc), null=True),
        ),
    ]

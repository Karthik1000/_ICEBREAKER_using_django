# Generated by Django 2.1.1 on 2018-11-08 19:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_auto_20181109_0101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 11, 8, 19, 36, 48, 526513, tzinfo=utc), null=True),
        ),
    ]

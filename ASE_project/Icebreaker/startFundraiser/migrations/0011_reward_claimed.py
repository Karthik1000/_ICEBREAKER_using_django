# Generated by Django 2.1.2 on 2018-12-09 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startFundraiser', '0010_reward_delivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='reward',
            name='claimed',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
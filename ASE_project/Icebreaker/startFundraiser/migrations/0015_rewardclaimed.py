# Generated by Django 2.0.5 on 2018-12-11 14:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('startFundraiser', '0014_auto_20181211_1509'),
    ]

    operations = [
        migrations.CreateModel(
            name='RewardClaimed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reward', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='startFundraiser.Reward')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
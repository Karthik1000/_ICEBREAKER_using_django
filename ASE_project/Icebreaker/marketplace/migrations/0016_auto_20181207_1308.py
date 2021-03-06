# Generated by Django 2.0.5 on 2018-12-07 07:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('marketplace', '0015_auto_20181202_1528'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_code', models.CharField(max_length=20)),
                ('is_ordered', models.BooleanField(default=False)),
                ('date_ordered', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_ordered', models.BooleanField(default=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_ordered', models.DateTimeField(null=True)),
                ('qty', models.IntegerField(default=1, null=True)),
                ('ref_code', models.CharField(max_length=20)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='marketplace.product')),
            ],
        ),
        migrations.RemoveField(
            model_name='cart',
            name='product',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='user',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='marketplace.OrderItem'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='o', to=settings.AUTH_USER_MODEL),
        ),
    ]

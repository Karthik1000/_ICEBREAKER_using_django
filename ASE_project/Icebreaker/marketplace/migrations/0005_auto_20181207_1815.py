# Generated by Django 2.0.6 on 2018-12-07 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0004_auto_20181207_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(max_length=5, null=True),
        ),
    ]

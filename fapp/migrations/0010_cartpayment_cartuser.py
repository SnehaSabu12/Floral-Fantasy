# Generated by Django 5.0.4 on 2024-07-25 10:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fapp', '0009_cartpayment_farmer_cartpayment_fremail_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartpayment',
            name='cartuser',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='fapp.user'),
            preserve_default=False,
        ),
    ]

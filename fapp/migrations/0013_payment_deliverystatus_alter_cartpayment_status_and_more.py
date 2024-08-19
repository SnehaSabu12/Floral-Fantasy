# Generated by Django 5.0.6 on 2024-08-10 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fapp', '0012_addproduct_stock_alter_cartpayment_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='deliverystatus',
            field=models.CharField(choices=[('pending', 'Pending'), ('delivered', 'Delivered')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='cartpayment',
            name='status',
            field=models.CharField(default='created', max_length=20),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(default='created', max_length=20),
        ),
    ]

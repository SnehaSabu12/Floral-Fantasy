# Generated by Django 5.0.4 on 2024-07-12 07:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='farmer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=50)),
                ('phonenumber', models.IntegerField()),
                ('bankname', models.CharField(max_length=30)),
                ('accountnumber', models.IntegerField()),
                ('ifsccode', models.CharField(max_length=15)),
                ('username', models.CharField(max_length=15)),
                ('email', models.EmailField(default='farmer@gmail.com', max_length=254)),
                ('password', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to='')),
                ('flicense', models.ImageField(upload_to='')),
                ('status', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='rply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=1000)),
                ('name', models.CharField(max_length=15)),
                ('email', models.EmailField(default='users@gmail.com', max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=50)),
                ('phonenumber', models.IntegerField()),
                ('bankname', models.CharField(max_length=30)),
                ('accountnumber', models.IntegerField()),
                ('ifsccode', models.CharField(max_length=15)),
                ('username', models.CharField(max_length=15)),
                ('email', models.EmailField(default='users@gmail.com', max_length=254)),
                ('password', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='addproduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=1000)),
                ('price', models.IntegerField()),
                ('image', models.ImageField(upload_to='')),
                ('frname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fapp.farmer')),
            ],
        ),
        migrations.CreateModel(
            name='PasswordResetFarm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('farm', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='fapp.farmer')),
            ],
        ),
        migrations.CreateModel(
            name='PasswordResetUsr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('usr', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='fapp.user')),
            ],
        ),
        migrations.CreateModel(
            name='feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=1000)),
                ('fdetail', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='fapp.farmer')),
                ('udetail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fapp.user')),
            ],
        ),
        migrations.CreateModel(
            name='cont',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=1000)),
                ('usrdetail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fapp.user')),
            ],
        ),
        migrations.CreateModel(
            name='cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now=True)),
                ('tprice', models.IntegerField(default=0)),
                ('cartitm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='fapp.addproduct')),
                ('user_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fapp.user')),
            ],
        ),
        migrations.CreateModel(
            name='buy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(default=0)),
                ('datee', models.DateTimeField(auto_now=True)),
                ('totprice', models.IntegerField(default=0)),
                ('buyitm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buy', to='fapp.addproduct')),
                ('userdetails', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fapp.user')),
            ],
        ),
    ]

# Generated by Django 5.1.5 on 2025-02-21 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Present',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('classes', models.CharField(max_length=15)),
                ('studentname', models.CharField(max_length=150)),
                ('roll', models.CharField(max_length=150)),
                ('college', models.CharField(max_length=150)),
                ('mobile', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studentname', models.CharField(max_length=150, unique=True)),
                ('roll', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.CharField(max_length=15, unique=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('address', models.CharField(max_length=105)),
                ('classes', models.CharField(max_length=15)),
                ('blood', models.CharField(max_length=15)),
                ('college', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=255)),
                ('status', models.CharField(default='Waiting', max_length=100)),
                ('qr', models.ImageField(blank=True, null=True, upload_to='qrcodes/')),
            ],
        ),
    ]

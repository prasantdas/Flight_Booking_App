# Generated by Django 5.0.1 on 2024-06-01 18:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0007_alter_flight_flight_number'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MyBookings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_location', models.CharField(max_length=100)),
                ('to_location', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('flight_number', models.CharField(max_length=20)),
                ('fare', models.DecimalField(decimal_places=2, max_digits=10)),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 5.0.1 on 2024-06-01 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0009_remove_mybookings_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mybookings',
            name='booking_date',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='mybookings',
            name='fare',
            field=models.CharField(max_length=20),
        ),
    ]
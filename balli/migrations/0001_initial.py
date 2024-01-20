# Generated by Django 5.0.1 on 2024-01-20 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CropTimeline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crop_type', models.CharField(choices=[('onion', 'प्याज'), ('tomato', 'टमाटर'), ('rice', 'धान')], max_length=100, unique=True)),
                ('ideal_starting_temperature', models.FloatField(blank=True, null=True)),
                ('ideal_starting_moisture', models.FloatField(blank=True, null=True)),
                ('pesticide_time', models.DateTimeField()),
                ('migration_time', models.DateTimeField(blank=True, null=True)),
                ('initial_moisture', models.FloatField()),
                ('initial_temperature', models.FloatField()),
                ('harvesting_time', models.DateTimeField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('edited_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
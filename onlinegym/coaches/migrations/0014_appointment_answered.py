# Generated by Django 5.1.4 on 2025-03-07 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coaches', '0013_appointment_workoutplan'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='answered',
            field=models.BooleanField(default=False),
        ),
    ]

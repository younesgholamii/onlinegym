# Generated by Django 5.1.4 on 2025-04-13 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coaches', '0014_appointment_answered'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='answered',
        ),
        migrations.AddField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('answered', 'answered')], default='pending', max_length=50),
        ),
    ]

# Generated by Django 5.1.4 on 2025-01-14 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_user_date_of_birth_remove_user_height_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_coach',
            field=models.BooleanField(default=False),
        ),
    ]

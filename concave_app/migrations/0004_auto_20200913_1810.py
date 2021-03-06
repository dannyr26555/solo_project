# Generated by Django 3.0.8 on 2020-09-13 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concave_app', '0003_convention_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendee',
            name='is_organizer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='organizer',
            name='is_organizer',
            field=models.BooleanField(default=True),
        ),
    ]

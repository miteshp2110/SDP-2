# Generated by Django 5.0.3 on 2024-03-11 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0004_userdata_assignedtask_userdata_selftask'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='notification',
            field=models.JSONField(blank=True, default={'notifications': []}),
        ),
    ]

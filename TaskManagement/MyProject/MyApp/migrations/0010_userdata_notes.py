# Generated by Django 5.0.3 on 2024-04-26 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0009_alluser_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='notes',
            field=models.JSONField(blank=True, default={'notes': []}),
        ),
    ]

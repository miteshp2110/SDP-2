# Generated by Django 4.2.8 on 2024-03-09 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='allUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userObj', models.JSONField(blank=True, default={'users': []})),
            ],
            options={
                'db_table': 'uList',
            },
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=150)),
                ('password', models.CharField(max_length=150)),
                ('connectionRequest', models.JSONField(blank=True, default={'requests': []})),
                ('activeConnections', models.JSONField(blank=True, default={'connections': []})),
            ],
            options={
                'db_table': 'Users',
            },
        ),
    ]

# Generated by Django 4.2.8 on 2024-03-09 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(default='123@gmail.com', max_length=254)),
                ('name', models.CharField(max_length=150)),
                ('password', models.CharField(max_length=150)),
                ('sessionId', models.CharField(blank=True, max_length=150)),
            ],
            options={
                'db_table': 'Users',
            },
        ),
    ]

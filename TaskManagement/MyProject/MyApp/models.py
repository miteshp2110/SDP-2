from django.db import models

# Create your models here.

class UserData(models.Model):
    email=models.EmailField(blank=False)
    name=models.CharField(blank=False,max_length=150)
    password=models.CharField(blank=False,max_length=150)

    class Meta:
        db_table="Users"


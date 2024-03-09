from django.db import models

# Create your models here.

class UserData(models.Model):
    email=models.EmailField(blank=False)
    name=models.CharField(blank=False,max_length=150)
    password=models.CharField(blank=False,max_length=150)


    connectionRequest=models.JSONField(blank=True,default={'requests':[]})
    activeConnections=models.JSONField(blank=True,default={'connections':[]})
    class Meta:
        db_table="Users"

class allUser(models.Model):
    userObj=models.JSONField(blank=True,default={'users':[]})

    class Meta:
        db_table='uList'












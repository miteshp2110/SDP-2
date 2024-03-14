from django.db import models

# Create your models here.

class UserData(models.Model):
    email=models.EmailField(blank=False)
    name=models.CharField(blank=False,max_length=150)
    password=models.CharField(blank=False,max_length=150)
    sessionId=models.CharField(blank=True,max_length=150)



    assignedTask=models.JSONField(blank=True,default={'tasks':[]})
    selfTask=models.JSONField(blank=True,default={'tasks':[]})
    connectionSent=models.JSONField(blank=True,default={'requests':[]})
    connectionRecieved=models.JSONField(blank=True,default={'requests':[]})
    activeConnections=models.JSONField(blank=True,default={'connections':[]})
    notification=models.JSONField(blank=True,default={'notifications':[]})
    class Meta:
        db_table="Users"

class allUser(models.Model):
    userObj=models.JSONField(blank=True,default={'users':[]})

    class Meta:
        db_table='uList'














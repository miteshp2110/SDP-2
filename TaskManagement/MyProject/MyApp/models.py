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
    notes=models.JSONField(blank=True,default={'notes':[]})
    updationQueue=models.JSONField(blank=True,default={'queue':[]})
    class Meta:
        db_table="Users"

class allUser(models.Model):
    userObj=models.JSONField(blank=True,default={'users':[]})
    feedback=models.JSONField(blank=True,default={'feedbacks':[]})

    class Meta:
        db_table='uList'

class adminUser(models.Model):
    email = models.EmailField(blank=False)
    name = models.CharField(blank=False, max_length=150)
    password = models.CharField(blank=False, max_length=150)

    class Meta:
        db_table='admins'












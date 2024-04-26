from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.UserData)
admin.site.register(models.allUser)
admin.site.register(models.adminUser)

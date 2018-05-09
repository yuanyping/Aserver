from django.contrib import admin

# Register your models here.
from file_ftp import models
admin.site.register(models.user_info)
admin.site.register(models.project)
admin.site.register(models.file_admin)


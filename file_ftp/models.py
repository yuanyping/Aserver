from django.db import models

# Create your models here.
class user_info(models.Model):
    user_name=models.CharField(max_length=8,null=False,verbose_name="用户名")
    user_pwd=models.CharField(max_length=16,null=False,verbose_name="用户密码")
    user_project=models.ManyToManyField(to="project")
    choice=((1,"管理员"),
            (2,"普通用户"))
    user_permission=models.IntegerField(choices=choice)

    def __str__(self):
        return self.user_name
class project(models.Model):
    project_name=models.CharField(max_length=255,null=False,verbose_name='项目名称')

    def __str__(self):
        return self.project_name

class file_admin(models.Model):
    file_name=models.CharField(max_length=255,null=True)
    file_download=models.CharField(max_length=255,null=True)
    file_md5=models.CharField(max_length=255,null=True)
    file_time=models.CharField(max_length=32)
    file_dir=models.CharField(max_length=32,default="abc")
    file_num=models.CharField(max_length=255)
    file_project=models.ManyToManyField(to="project")
    file_owner=models.ManyToManyField(to="user_info")
    def __str__(self):
        return self.file_name

# Generated by Django 2.0.2 on 2018-05-07 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_ftp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_info',
            name='user_permission',
            field=models.IntegerField(choices=[(1, '管理员'), (2, '普通用户')], default=2),
            preserve_default=False,
        ),
    ]

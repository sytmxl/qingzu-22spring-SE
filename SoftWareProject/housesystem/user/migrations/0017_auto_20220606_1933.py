# Generated by Django 3.2.5 on 2022-06-06 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_work_orderid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='PicID',
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.FileField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='user',
            name='avatar_url',
            field=models.CharField(default='', max_length=255, null=True),
        ),
    ]

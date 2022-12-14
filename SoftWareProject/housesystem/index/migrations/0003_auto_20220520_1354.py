# Generated by Django 3.2.5 on 2022-05-20 05:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20220518_1435'),
        ('index', '0002_remove_picture_picpath'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picture',
            name='Picture_House',
        ),
        migrations.RemoveField(
            model_name='picture',
            name='Picture_Work',
        ),
        migrations.AddField(
            model_name='house',
            name='House_Picture',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='index.picture'),
        ),
        migrations.AlterField(
            model_name='house',
            name='House_Collection',
            field=models.ManyToManyField(null=True, to='user.User'),
        ),
        migrations.AlterField(
            model_name='info',
            name='Info_User',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
        migrations.AlterField(
            model_name='info',
            name='Info_Work',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.work'),
        ),
    ]

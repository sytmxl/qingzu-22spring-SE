# Generated by Django 3.2.5 on 2022-05-27 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0006_rename_mark_house_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='City',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='house',
            name='Status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='picture',
            name='PicPath',
            field=models.CharField(max_length=255, null=True),
        ),
    ]

# Generated by Django 3.2.5 on 2022-05-25 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20220525_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userhouse',
            name='HouseID',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='userhouse',
            name='UserID',
            field=models.IntegerField(),
        ),
    ]

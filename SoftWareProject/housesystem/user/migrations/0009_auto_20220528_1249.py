# Generated by Django 3.2.5 on 2022-05-28 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20220527_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='Comment',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='Mark',
            field=models.IntegerField(null=True),
        ),
    ]

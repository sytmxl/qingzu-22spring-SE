# Generated by Django 3.2.5 on 2022-06-06 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_contract_passed_user_workid'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='OrderID',
            field=models.IntegerField(null=True),
        ),
    ]

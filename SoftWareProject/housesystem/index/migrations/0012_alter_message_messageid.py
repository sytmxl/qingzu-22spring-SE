# Generated by Django 3.2.5 on 2022-06-01 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0011_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='MessageID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]

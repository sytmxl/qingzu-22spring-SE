# Generated by Django 3.2.5 on 2022-06-07 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0020_auto_20220607_1320'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contract',
            old_name='File_url',
            new_name='FilePath',
        ),
    ]

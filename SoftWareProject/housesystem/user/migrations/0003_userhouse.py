# Generated by Django 3.2.5 on 2022-05-20 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0004_auto_20220520_1440'),
        ('user', '0002_auto_20220518_1435'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserHouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('HouseID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.house')),
                ('UserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
    ]

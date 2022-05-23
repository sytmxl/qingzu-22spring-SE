# Generated by Django 3.2.5 on 2022-05-18 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('ContractID', models.IntegerField(primary_key=True, serialize=False)),
                ('OrderID', models.IntegerField()),
                ('FilePath', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('OrderID', models.IntegerField(primary_key=True, serialize=False)),
                ('OrderDate', models.DateTimeField()),
                ('DueDate', models.DateTimeField()),
                ('Price', models.IntegerField()),
                ('Mark', models.IntegerField()),
                ('Comment', models.CharField(max_length=50)),
                ('Pay', models.BooleanField()),
                ('UserID', models.IntegerField()),
                ('HouseID', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('UserID', models.IntegerField(primary_key=True, serialize=False)),
                ('Email', models.CharField(max_length=255)),
                ('UserName', models.CharField(max_length=255)),
                ('Password', models.CharField(max_length=255)),
                ('PicID', models.CharField(max_length=255, null=True)),
                ('ID', models.CharField(max_length=18, null=True)),
                ('Phone', models.CharField(max_length=11, null=True)),
                ('Status', models.CharField(max_length=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('WorkID', models.IntegerField(primary_key=True, serialize=False)),
                ('Datatime', models.DateTimeField()),
                ('HouseID', models.IntegerField()),
                ('Description', models.CharField(max_length=255)),
                ('UserID', models.IntegerField()),
                ('WorkerID', models.IntegerField()),
                ('Comment', models.CharField(max_length=255, null=True)),
                ('Mark', models.IntegerField(null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='members',
        ),
    ]
